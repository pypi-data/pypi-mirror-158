# -*- coding: utf-8 eval: (blacken-mode 1) -*-
#
# October 1 2021, Christian Hopps <chopps@labn.net>
#
# Copyright (c) 2021-2022, LabN Consulting, L.L.C.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; see the file COPYING; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#
"A module that defines objects for standalone use."
import asyncio
import ipaddress
import logging
import os
import random
import re
import shlex
import subprocess

from . import cli
from .base import BaseMunet
from .base import Bridge
from .base import LinuxNamespace
from .base import Timeout
from .base import _async_get_exec_path
from .base import _get_exec_path
from .base import cmd_error
from .base import get_exec_path_host
from .config import config_subst
from .config import config_to_dict_with_key
from .config import find_matching_net_config
from .config import merge_kind_config


def get_loopback_ips(c, nid):
    if ip := c.get("ip"):
        if ip == "auto":
            return [ipaddress.ip_interface("10.255.0.0/32") + nid]
        if isinstance(ip, str):
            return [ipaddress.ip_interface(ip)]
        return [ipaddress.ip_interface(x) for x in ip]
    return []


def make_ip_network(net, inc):
    n = ipaddress.ip_network(net)
    return ipaddress.ip_network(
        (n.network_address + inc * n.num_addresses, n.prefixlen)
    )


def get_ip_network(c, brid):
    ip = c.get("ip")
    if ip and str(ip) != "auto":
        try:
            ifip = ipaddress.ip_interface(ip)
            if ifip.ip == ifip.network.network_address:
                return ifip.network
            return ifip
        except ValueError:
            return ipaddress.ip_network(ip)
    return make_ip_network("10.0.0.0/24", brid)


async def to_thread(func):
    """to_thread for python < 3.9"""
    try:
        return await asyncio.to_thread(func)
    except AttributeError:
        logging.warning("Using backport to_thread")
        return await asyncio.get_running_loop().run_in_executor(None, func)


class L2Bridge(Bridge):
    """
    A linux bridge with no IP network address.
    """

    def __init__(self, name=None, unet=None, logger=None, config=None):
        """Create a linux Bridge."""

        super().__init__(name=name, unet=unet, logger=logger)

        self.config = config if config else {}


class L3Bridge(Bridge):
    """
    A linux bridge with associated IP network address.
    """

    def __init__(self, name=None, unet=None, logger=None, config=None):
        """Create a linux Bridge."""

        super().__init__(name=name, unet=unet, logger=logger)

        self.config = config if config else {}

        self.ip_interface = get_ip_network(self.config, self.id)
        if hasattr(self.ip_interface, "network"):
            self.ip_address = self.ip_interface.ip
            self.ip_network = self.ip_interface.network
            self.cmd_raises(f"ip addr add {self.ip_interface} dev {name}")
        else:
            self.ip_address = None
            self.ip_network = self.ip_interface

        self.logger.debug("%s: set network address to %s", self, self.ip_interface)

        self.is_nat = self.config.get("nat", False)
        if self.is_nat:
            self.cmd_raises(
                "iptables -t nat -A POSTROUTING "
                f"-s {self.ip_network} ! -o {self.name} -j MASQUERADE"
            )

    async def async_delete(self):
        if type(self) == L3Bridge:  # pylint: disable=C0123
            self.logger.info("%s: deleting", self)
        else:
            self.logger.debug("%s: L3Bridge sub-class async_delete", self)

        if self.config.get("nat", False):
            self.cmd_status(
                "iptables -t nat -D POSTROUTING "
                f"-s {self.ip_network} ! -o {self.name} -j MASQUERADE"
            )

        await super().async_delete()


class L3Node(LinuxNamespace):
    """
    A linux namespace with IP attributes.
    """

    next_ord = 1

    @classmethod
    def _get_next_ord(cls):
        # Do not use `cls` here b/c that makes the variable class specific
        n = L3Node.next_ord
        L3Node.next_ord = n + 1
        return n

    def __init__(self, name, config=None, unet=None, **kwargs):
        """Create a linux Bridge."""

        self.config = config if config else {}
        config = self.config

        self.cmd_p = None
        self.container_id = ""
        self.id = int(config["id"]) if "id" in config else self._get_next_ord()
        assert unet is not None
        self.unet = unet

        self.intf_tc_count = 0

        if not name:
            name = "r{}".format(self.id)
        super().__init__(name=name, **kwargs)

        self.mount_volumes()

        # -----------------------
        # Setup node's networking
        # -----------------------
        if not self.unet.ipv6_enable:
            # Disable IPv6
            self.cmd_raises("sysctl -w net.ipv6.conf.all.autoconf=0")
            self.cmd_raises("sysctl -w net.ipv6.conf.all.disable_ipv6=1")

        self.next_p2p_network = ipaddress.ip_network(f"10.254.{self.id}.0/31")

        self.loopback_ip = None
        self.loopback_ips = get_loopback_ips(self.config, self.id)
        self.loopback_ip = self.loopback_ips[0] if self.loopback_ips else None
        if self.loopback_ip:
            self.cmd_raises_host(f"ip addr add {self.loopback_ip} dev lo")
            self.cmd_raises_host("ip link set lo up")
            for i, ip in enumerate(self.loopback_ips[1:]):
                self.cmd_raises_host(f"ip addr add {ip} dev lo:{i}")

        # -------------------
        # Setup node's rundir
        # -------------------

        self.rundir = os.path.join(unet.rundir, name)
        self.cmd_raises_host(f"mkdir -p {self.rundir}")
        # Not host path based, but we assume same
        self.set_cwd(self.rundir)

        # Save the namespace pid
        with open(os.path.join(self.rundir, "nspid"), "w", encoding="ascii") as f:
            f.write(f"{self.pid}\n")

        hosts_file = os.path.join(self.rundir, "hosts.txt")
        if os.path.exists(hosts_file):
            self.bind_mount(hosts_file, "/etc/hosts")

        if not self.is_container:
            self.pytest_hook_open_shell()

    async def console(
        self,
        concmd,
        prompt=r"(^|\r\n)[^#\$]*[#\$] ",
        user=None,
        password=None,
        use_pty=False,
        noecho=False,
        trace=True,
    ):
        lfname = os.path.join(self.rundir, "console-log.txt")
        logfile = open(lfname, "a+", encoding="utf-8")
        logfile.write("-- start logging for: '{}' --\n".format(concmd))

        lfname = os.path.join(self.rundir, "console-read-log.txt")
        logfile_read = open(lfname, "a+", encoding="utf-8")
        logfile_read.write("-- start read logging for: '{}' --\n".format(concmd))

        lfname = os.path.join(self.rundir, "console-send-log.txt")
        logfile_send = open(lfname, "a+", encoding="utf-8")
        logfile_send.write("-- start send logging for: '{}' --\n".format(concmd))

        expects = []
        sends = []
        if user:
            expects.append("ogin:")
            sends.append(user + "\n")
        if password is not None:
            expects.append("assword:")
            sends.append(password + "\n")
        repl = await self.shell_spawn(
            concmd,
            prompt,
            expects,
            sends,
            logfile=logfile,
            use_pty=use_pty,
            logfile_read=logfile_read,
            logfile_send=logfile_send,
            noecho=noecho,
            trace=trace,
        )
        return repl

    def mount_volumes(self):
        for m in self.config.get("volumes", []):
            if isinstance(m, str):
                s = m.split(":", 1)
                if len(s) == 1:
                    self.tmpfs_mount(s[0])
                else:
                    spath = s[0]
                    if spath[0] == ".":
                        spath = os.path.abspath(
                            os.path.join(self.unet.config_dirname, spath)
                        )
                    self.bind_mount(spath, s[1])
                continue
            raise NotImplementedError("complex mounts for non-containers")

    def get_ifname(self, netname):
        for c in self.config["connections"]:
            if c["to"] == netname:
                return c["name"]
        return None

    async def run_cmd(self):
        """Run the configured commands for this node"""

        self.logger.debug(
            "[rundir %s exists %s]", self.rundir, os.path.exists(self.rundir)
        )

        shell_cmd = self.config.get("shell", "/bin/bash")
        cmd = self.config.get("cmd", "").strip()
        if not cmd:
            return None

        # See if we have a custom update for this `kind`
        if kind := self.config.get("kind", None):
            if kind in kind_run_cmd_update:
                await kind_run_cmd_update[kind](self, shell_cmd, [], cmd)

        if shell_cmd:
            if not isinstance(shell_cmd, str):
                shell_cmd = "/bin/bash"
            if cmd.find("\n") == -1:
                cmd += "\n"
            cmdpath = os.path.join(self.rundir, "cmd.shebang")
            with open(cmdpath, mode="w+", encoding="utf-8") as cmdfile:
                cmdfile.write(f"#!{shell_cmd}\n")
                cmdfile.write(cmd)
                cmdfile.flush()
            self.cmd_raises_host(f"chmod 755 {cmdpath}")
            cmds = [cmdpath]
        else:
            cmds = shlex.split(cmd)

        stdout = open(os.path.join(self.rundir, "cmd.out"), "wb")
        stderr = open(os.path.join(self.rundir, "cmd.err"), "wb")
        self.cmd_p = await self.async_popen(
            cmds,
            stdin=subprocess.DEVNULL,
            stdout=stdout,
            stderr=stderr,
            start_new_session=True,  # allows us to signal all children to exit
        )

        self.logger.debug(
            "%s: async_popen %s => %s",
            self,
            cmds,
            self.cmd_p.pid,
        )

        self.pytest_hook_run_cmd(stdout, stderr)

        return self.cmd_p

    def cmd_completed(self, future):
        self.logger.debug("%s: cmd completed called", self)
        try:
            n = future.result()
            self.logger.debug("%s: node cmd completed result: %s", self, n)
        except asyncio.CancelledError:
            # Should we stop the container if we have one?
            self.logger.debug("%s: node cmd wait() canceled", future)

    # def child_exit(self, pid):
    #     """Called back when cmd finishes executing."""
    #     if self.cmd_p && self.cmd_p.pid == pid:
    #         self.container_id = None

    def set_lan_addr(self, switch, cconf):
        if ip := cconf.get("ip"):
            ipaddr = ipaddress.ip_interface(ip)
        elif self.unet.autonumber and "ip" not in cconf:
            self.logger.debug(
                "%s: prefixlen of switch %s is %s",
                self,
                switch.name,
                switch.ip_network.prefixlen,
            )
            n = switch.ip_network
            ipaddr = ipaddress.ip_interface((n.network_address + self.id, n.prefixlen))
        else:
            return

        ifname = cconf["name"]
        self.intf_addrs[ifname] = ipaddr
        self.logger.debug("%s: adding %s to lan intf %s", self, ipaddr, ifname)
        self.intf_ip_cmd(ifname, f"ip addr add {ipaddr} dev {ifname}")

        if hasattr(switch, "is_nat") and switch.is_nat:
            self.cmd_raises(f"ip route add default via {switch.ip_address}")

    def pytest_hook_run_cmd(self, stdout, stderr):
        if not self.unet or not self.unet.pytest_config:
            return

        outopt = self.unet.pytest_config.getoption("--stdout")
        outopt = outopt if outopt is not None else ""
        if outopt == "all" or self.name in outopt.split(","):
            self.run_in_window(f"tail -F {stdout.name}", title=f"O:{self.name}")

        erropt = self.unet.pytest_config.getoption("--stderr")
        erropt = erropt if erropt is not None else ""
        if erropt == "all" or self.name in erropt.split(","):
            self.run_in_window(f"tail -F {stderr.name}", title=f"E:{self.name}")

    def pytest_hook_open_shell(self):
        if not self.unet or not self.unet.pytest_config:
            return
        shellopt = self.unet.pytest_config.getoption("--shell")
        shellopt = shellopt if shellopt is not None else ""
        if shellopt == "all" or self.name in shellopt.split(","):
            self.run_in_window("bash")

    def set_p2p_addr(self, other, cconf, occonf):
        ipaddr = ipaddress.ip_interface(cconf["ip"]) if cconf.get("ip") else None
        oipaddr = ipaddress.ip_interface(occonf["ip"]) if occonf.get("ip") else None

        if not ipaddr and not oipaddr:
            if self.unet.autonumber:
                n = self.next_p2p_network
                self.next_p2p_network = make_ip_network(n, 1)

                ipaddr = ipaddress.ip_interface(n)
                oipaddr = ipaddress.ip_interface((ipaddr.ip + 1, n.prefixlen))
            else:
                return

        if ipaddr:
            ifname = cconf["name"]
            self.intf_addrs[ifname] = ipaddr
            self.logger.debug("%s: adding %s to p2p intf %s", self, ipaddr, ifname)
            self.intf_ip_cmd(ifname, f"ip addr add {ipaddr} dev {ifname}")

        if oipaddr:
            oifname = occonf["name"]
            other.intf_addrs[oifname] = oipaddr
            self.logger.debug(
                "%s: adding %s to other p2p intf %s", other, oipaddr, oifname
            )
            other.intf_ip_cmd(oifname, f"ip addr add {oipaddr} dev {oifname}")

    async def async_delete(self):
        if type(self) == L3Node:  # pylint: disable=C0123
            # Used to use info here as the top level delete but the user doesn't care,
            # right?
            self.logger.info("%s: deleting", self)
        else:
            self.logger.debug("%s: L3Node sub-class async_delete", self)
        await self.async_cleanup_proc(self.cmd_p)
        await super().async_delete()


class L3ContainerNode(L3Node):
    """
    An container (podman) based L3Node.
    """

    def __init__(self, name, config, **kwargs):
        """Create a Container Node."""
        self.cont_exec_paths = {}
        self.container_id = None
        self.container_image = config["image"]
        self.extra_mounts = []
        assert self.container_image

        super().__init__(
            name=name,
            config=config,
            # cgroup=True,
            # pid=True,
            # private_mounts=["/sys/fs/cgroup:/sys/fs/cgroup"],
            **kwargs,
        )

    @property
    def is_container(self):
        return True

    def get_exec_path(self, binary):
        """Return the full path to the binary executable inside the image.

        `binary` :: binary name or list of binary names
        """
        return _get_exec_path(binary, self.cmd_status, self.cont_exec_paths)

    async def async_get_exec_path(self, binary):
        """Return the full path to the binary executable inside the image.

        `binary` :: binary name or list of binary names
        """
        path = await _async_get_exec_path(
            binary, self.async_cmd_status, self.cont_exec_paths
        )
        return path

    def get_exec_path_host(self, binary):
        """Return the full path to the binary executable on the host.

        `binary` :: binary name or list of binary names
        """
        return get_exec_path_host(binary)

    def _get_podman_precmd(self, cmd, sudo=False, tty=False):
        cmds = []
        if sudo:
            cmds.append(get_exec_path_host("sudo"))
        cmds.append(get_exec_path_host("podman"))
        if self.container_id:
            cmds.append("exec")
            cmds.append(f"-eMUNET_RUNDIR={self.unet.rundir}")
            cmds.append(f"-eMUNET_NODENAME={self.name}")
            if tty:
                cmds.append("-it")
            cmds.append(self.container_id)
        else:
            cmds += [
                "run",
                "--rm",
                "--init",
                f"-eMUNET_RUNDIR={self.unet.rundir}",
                f"-eMUNET_NODENAME={self.name}",
                f"--net=ns:/proc/{self.pid}/ns/net",
            ]
            if tty:
                cmds.append("-it")
            cmds.append(self.container_image)
        if not isinstance(cmd, str):
            cmds += cmd
        else:
            # Make sure the code doesn't think `cd` will work.
            assert not re.match(r"cd(\s*|\s+(\S+))$", cmd)
            cmds += ["/bin/bash", "-c", cmd]
        return cmds

    def get_cmd_container(self, cmd, sudo=False, tty=False):
        # return " ".join(self._get_podman_precmd(cmd, sudo=sudo, tty=tty))
        return self._get_podman_precmd(cmd, sudo=sudo, tty=tty)

    def popen(self, cmd, **kwargs):
        """
        Creates a pipe with the given `command`.

        Args:
            cmd: `str` or `list` of command to open a pipe with.
            **kwargs: kwargs is eventually passed on to Popen. If `command` is a string
                then will be invoked with `bash -c`, otherwise `command` is a list and
                will be invoked without a shell.

        Returns:
            a subprocess.Popen object.
        """
        if not self.cmd_p:
            return super().popen(cmd, **kwargs)
        # By default do not run inside container
        skip_pre_cmd = kwargs.get("skip_pre_cmd", True)
        # Never use the base class nsenter precmd
        kwargs["skip_pre_cmd"] = True
        cmds = cmd if skip_pre_cmd else self._get_podman_precmd(cmd)
        p, _ = self._popen("popen", cmds, **kwargs)
        return p

    async def async_popen(self, cmd, **kwargs):
        if not self.cmd_p:
            return await super().async_popen(cmd, **kwargs)
        # By default do not run inside container
        skip_pre_cmd = kwargs.get("skip_pre_cmd", True)
        # Never use the base class nsenter precmd
        kwargs["skip_pre_cmd"] = True
        cmds = cmd if skip_pre_cmd else self._get_podman_precmd(cmd)
        p, _ = await self._async_popen("async_popen", cmds, **kwargs)
        return p

    def cmd_status(self, cmd, **kwargs):
        if not self.cmd_p:
            return super().cmd_status(cmd, **kwargs)
        if tty := kwargs.get("tty", False):
            # tty always runs inside container (why?)
            skip_pre_cmd = False
            del kwargs["tty"]
        else:
            # By default run inside container
            skip_pre_cmd = kwargs.get("skip_pre_cmd", False)
        # Never use the base class nsenter precmd
        kwargs["skip_pre_cmd"] = True
        cmds = cmd if skip_pre_cmd else self._get_podman_precmd(cmd, tty)
        cmds = self.cmd_get_cmd_list(cmds)
        return self._cmd_status(cmds, **kwargs)

    async def async_cmd_status(self, cmd, **kwargs):
        if not self.cmd_p:
            return await super().async_cmd_status(cmd, **kwargs)
        if tty := kwargs.get("tty", False):
            # tty always runs inside container (why?)
            skip_pre_cmd = False
            del kwargs["tty"]
        else:
            # By default run inside container
            skip_pre_cmd = kwargs.get("skip_pre_cmd", False)
        # Never use the base class nsenter precmd
        kwargs["skip_pre_cmd"] = True
        cmds = cmd if skip_pre_cmd else self._get_podman_precmd(cmd, tty)
        cmds = self.cmd_get_cmd_list(cmds)
        return await self._async_cmd_status(cmds, **kwargs)

    def tmpfs_mount(self, inner):
        # eventually would be nice to support live mounting
        assert not self.container_id
        self.logger.debug("Mounting tmpfs on %s", inner)
        self.extra_mounts.append(f"--mount=type=tmpfs,destination={inner}")

    def bind_mount(self, outer, inner):
        # eventually would be nice to support live mounting
        assert not self.container_id
        self.logger.debug("Bind mounting %s on %s", outer, inner)
        if not self.test_host("-e", outer):
            self.cmd_raises(f"mkdir -p {outer}")
        self.extra_mounts.append(f"--mount=type=bind,src={outer},dst={inner}")

    def mount_volumes(self):
        args = []
        for m in self.config.get("volumes", []):
            if isinstance(m, str):
                s = m.split(":", 1)
                if len(s) == 1:
                    args.append("--mount=type=tmpfs,destination=" + m)
                else:
                    spath = s[0]
                    spath = os.path.abspath(
                        os.path.join(
                            os.path.dirname(self.unet.config["config_pathname"]), spath
                        )
                    )
                    if not self.test_host("-e", spath):
                        self.cmd_raises(f"mkdir -p {spath}")
                    args.append(f"--mount=type=bind,src={spath},dst={s[1]}")
                continue

        for m in self.config.get("mounts", []):
            margs = ["type=" + m["type"]]
            for k, v in m.items():
                if k == "type":
                    continue
                if v:
                    if k in ("src", "source"):
                        v = os.path.abspath(
                            os.path.join(
                                os.path.dirname(self.unet.config["config_pathname"]), v
                            )
                        )
                        if not self.test_host("-e", v):
                            self.cmd_raises(f"mkdir -p {v}")
                    margs.append(f"{k}={v}")
                else:
                    margs.append(f"{k}")
            args.append("--mount=" + ",".join(margs))

        if args:
            # Need to work on a way to mount into live container too
            self.extra_mounts += args

    async def run_cmd(self):
        """Run the configured commands for this node"""

        self.logger.debug("%s: starting container", self.name)
        self.logger.debug(
            "[rundir %s exists %s]", self.rundir, os.path.exists(self.rundir)
        )

        image = self.container_image

        self.container_id = f"{self.name}-{os.getpid()}"
        cmds = [
            get_exec_path_host("podman"),
            "run",
            f"--name={self.container_id}",
            f"--net=ns:/proc/{self.pid}/ns/net",
            f"--hostname={self.name}",
            f"--add-host={self.name}:127.0.0.1",
            # We can't use --rm here b/c podman fails on "stop".
            # u"--rm",
        ]

        if self.config.get("init", True):
            cmds.append("--init")

        if self.config.get("privileged", False):
            cmds.append("--privileged")
            # If we don't do this then the host file system is remounted read-only on
            # exit!
            cmds.append("--systemd=false")
        else:
            cmds.extend(
                [
                    # "--cap-add=SYS_ADMIN",
                    "--cap-add=NET_ADMIN",
                    "--cap-add=NET_RAW",
                ]
            )

        # Add volumes:
        if self.extra_mounts:
            cmds += self.extra_mounts

        # Add environment variables:
        envdict = self.config.get("env", {})
        if envdict is None:
            envdict = {}
        for k, v in envdict.items():
            cmds.append(f"--env={k}={v}")

        # Update capabilities
        cmds += [f"--cap-add={x}" for x in self.config.get("cap-add", [])]
        cmds += [f"--cap-drop={x}" for x in self.config.get("cap-drop", [])]
        # cmds += [f"--expose={x.split(':')[0]}" for x in self.config.get("ports", [])]
        cmds += [f"--publish={x}" for x in self.config.get("ports", [])]

        # Add extra flags from user:
        if "podman" in self.config:
            for x in self.config["podman"].get("extra-args", []):
                cmds.append(x.strip())

        shell_cmd = self.config.get("shell", "/bin/bash")
        cmd = self.config.get("cmd", "").strip()

        # See if we have a custom update for this `kind`
        if kind := self.config.get("kind", None):
            if kind in kind_run_cmd_update:
                cmds, cmd = await kind_run_cmd_update[kind](self, shell_cmd, cmds, cmd)

        if shell_cmd and cmd:
            if not isinstance(shell_cmd, str):
                shell_cmd = "/bin/bash"
            assert isinstance(cmd, str)
            # make cmd \n terminated for script
            cmd = cmd.rstrip()
            if cmd[-1] != "\n":
                cmd += "\n"
            cmdpath = os.path.join(self.rundir, "cmd.shebang")
            with open(cmdpath, mode="w+", encoding="utf-8") as cmdfile:
                cmdfile.write(f"#!{shell_cmd}\n")
                cmdfile.write(cmd)
                cmdfile.flush()
            self.cmd_raises_host(f"chmod 755 {cmdpath}")
            cmds += [
                # How can we override this?
                # u'--entrypoint=""',
                f"--volume={cmdpath}:/tmp/cmds.shebang",
                image,
                "/tmp/cmds.shebang",
            ]
        else:
            cmds.append(image)
            if cmd:
                if isinstance(cmd, str):
                    cmds.extend(shlex.split(cmd))
                else:
                    cmds.extend(cmd)

        stdout = open(os.path.join(self.rundir, "cmd.out"), "wb")
        stderr = open(os.path.join(self.rundir, "cmd.err"), "wb")
        self.cmd_p = await self.async_popen(
            cmds,
            stdin=subprocess.DEVNULL,
            stdout=stdout,
            stderr=stderr,
            # We don't need this here b/c we are only ever running podman and that's all
            # we need to kill for cleanup
            # start_new_session=True,  # allows us to signal all children to exit
            skip_pre_cmd=True,
        )

        self.logger.debug("%s: async_popen => %s", self, self.cmd_p.pid)

        self.pytest_hook_run_cmd(stdout, stderr)

        # ---------------------------------------
        # Now let's wait until container shows up
        # ---------------------------------------
        timeout = Timeout(30)
        while self.cmd_p.returncode is None and not timeout.is_expired():
            o = await self.async_cmd_raises_host(
                f"podman ps -q -f name={self.container_id}"
            )
            if o.strip():
                break
            elapsed = int(timeout.elapsed())
            if elapsed <= 3:
                await asyncio.sleep(0.1)
            else:
                self.logger.info("%s: run_cmd taking more than %ss", self, elapsed)
                await asyncio.sleep(1)
        if self.cmd_p.returncode is not None:
            self.logger.warning(
                "%s: run_cmd exited quickly (%ss) rc: %s",
                self,
                timeout.elapsed(),
                self.cmd_p.returncode,
            )
        elif timeout.is_expired():
            self.logger.critical(
                "%s: timeout (%ss) waiting for container to start",
                self.name,
                timeout.elapsed(),
            )
            assert not timeout.is_expired()

        self.logger.info("%s: started container", self.name)

        self.pytest_hook_open_shell()

        return self.cmd_p

    def cmd_completed(self, future):
        self.logger.debug("%s: cmd completed called", self)
        try:
            n = future.result()
            self.logger.debug("%s: node contianer cmd completed result: %s", self, n)
        except asyncio.CancelledError as error:
            # Should we stop the container if we have one?
            self.logger.debug(
                "%s: node container cmd wait() canceled: %s", future, error
            )

    async def async_delete(self):
        if type(self) == L3ContainerNode:  # pylint: disable=C0123
            # Used to use info here as the top level delete but the user doesn't care,
            # right?
            self.logger.info("%s: deleting", self)
        else:
            self.logger.debug("%s: L3ContainerNode delete", self)

        if contid := self.container_id:
            o = ""
            e = ""
            if self.cmd_p:
                if (rc := self.cmd_p.returncode) is None:
                    rc, o, e = await self.async_cmd_status_host(
                        [get_exec_path_host("podman"), "stop", contid]
                    )
                if rc and rc < 128:
                    self.logger.warning(
                        "%s: podman stop on cmd failed: %s",
                        self,
                        cmd_error(rc, o, e),
                    )
            # now remove the container
            rc, o, e = await self.async_cmd_status_host(
                [get_exec_path_host("podman"), "rm", contid]
            )
            if rc:
                self.logger.warning(
                    "%s: podman rm failed: %s", self, cmd_error(rc, o, e)
                )
            else:
                # It's gone
                self.cmd_p = None

        await super().async_delete()


class Munet(BaseMunet):
    """
    Munet.
    """

    def __init__(self, rundir=None, config=None, pytestconfig=None, **kwargs):
        super().__init__(**kwargs)

        self.rundir = rundir if rundir else "/tmp/unet-" + os.environ["USER"]
        self.cmd_raises(f"mkdir -p {self.rundir} && chmod 755 {self.rundir}")
        self.set_cwd(self.rundir)

        if not config:
            config = {}
        self.config = config
        if "config_pathname" in config:
            self.config_pathname = os.path.realpath(config["config_pathname"])
            self.config_dirname = os.path.dirname(self.config_pathname)
        else:
            self.config_pathname = ""
            self.config_dirname = ""

        self.pytest_config = pytestconfig

        # Save the namespace pid
        with open(os.path.join(self.rundir, "nspid"), "w", encoding="ascii") as f:
            f.write(f"{self.pid}\n")

        # Common CLI commands for any topology
        cdict = {
            "commands": [
                {
                    "name": "pcap",
                    "format": "pcap NETWORK",
                    "help": (
                        "capture packets from NETWORK into file capture-NETWORK.pcap"
                        " the command is run within a new window which also shows"
                        " packet summaries"
                    ),
                    "exec": "tshark -s 1508 -i {0} -P -w capture-{0}.pcap",
                    "top-level": True,
                    "new-window": {"background": True},
                },
                {
                    "name": "hterm",
                    "format": "hterm HOST [HOST ...]",
                    "help": (
                        "open terminal[s] on HOST[S] (outside containers), * for all"
                    ),
                    "exec": "bash",
                    "on-host": True,
                    "new-window": True,
                },
                {
                    "name": "term",
                    "format": "term HOST [HOST ...]",
                    "help": "open terminal[s] (TMUX or XTerm) on HOST[S], * for all",
                    "exec": "bash",
                    "new-window": True,
                },
                {
                    "name": "xterm",
                    "format": "xterm HOST [HOST ...]",
                    "help": "open XTerm[s] on HOST[S], * for all",
                    "exec": "bash",
                    "new-window": {
                        "forcex": True,
                    },
                },
                {
                    "name": "sh",
                    "format": "[HOST ...] sh <SHELL-COMMAND>",
                    "help": "execute <SHELL-COMMAND> on hosts",
                    "exec": "bash -c '{}'",
                },
                {
                    "name": "shi",
                    "format": "[HOST ...] shi <INTERACTIVE-COMMAND>",
                    "help": "execute <INTERACTIVE-COMMAND> on HOST[s]",
                    "exec": "bash -c '{}'",
                    "interactive": True,
                },
                {
                    "name": "stdout",
                    "exec": "tail -F %RUNDIR%/%NAME%/cmd.out",
                    "format": "stdout HOST [HOST ...]",
                    "help": "tail -f on the stdout of the cmd for this node",
                    "new-window": True,
                },
                {
                    "name": "stderr",
                    "exec": "tail -F %RUNDIR%/%NAME%/cmd.err",
                    "format": "stdout HOST [HOST ...]",
                    "help": "tail -f on the stdout of the cmd for this node",
                    "new-window": True,
                },
            ]
        }

        cli.add_cli_config(self, cdict)

        if "cli" in config:
            cli.add_cli_config(self, config["cli"])

        if "topology" not in self.config:
            self.config["topology"] = {}

        self.topoconf = self.config["topology"]
        self.ipv6_enable = self.topoconf.get("ipv6-enable", False)

        if self.isolated and not self.ipv6_enable:
            # Disable IPv6
            self.cmd_raises("sysctl -w net.ipv6.conf.all.autoconf=0")
            self.cmd_raises("sysctl -w net.ipv6.conf.all.disable_ipv6=1")

        self._build_topology(kwargs.get("logger"))

    def _build_topology(self, logger):
        # Allow for all networks to be auto-numbered
        topoconf = self.topoconf
        autonumber = self.autonumber

        kinds = self.config.get("kinds", {})

        for name, conf in config_to_dict_with_key(topoconf, "networks", "name").items():
            if kind := conf.get("kind"):
                if kconf := kinds[kind]:
                    conf = merge_kind_config(kconf, conf)
            conf = config_subst(conf, name=name, rundir=self.rundir)
            if "ip" not in conf and autonumber:
                conf["ip"] = "auto"
            topoconf["networks"][name] = conf
            self.add_network(name, conf, logger=logger)

        for name, conf in config_to_dict_with_key(topoconf, "nodes", "name").items():
            config_to_dict_with_key(
                conf, "env", "name"
            )  # convert list of env objects to dict

            if kind := conf.get("kind"):
                if kconf := kinds[kind]:
                    conf = merge_kind_config(kconf, conf)

            conf = config_subst(conf, name=name, rundir=self.rundir)
            topoconf["nodes"][name] = conf
            self.add_l3_node(name, conf, logger=logger)

        # Go through all connections and name them so they are sane to the user
        # otherwise when we do p2p links the names/ords skip around based oddly
        for name, node in self.hosts.items():
            nconf = node.config
            if "connections" not in nconf:
                continue
            nconns = []
            for cconf in nconf["connections"]:
                # Replace string only with a dictionary
                if isinstance(cconf, str):
                    cconf = cconf.split(":", 1)
                    cconf = {"to": cconf[0]}
                    if len(cconf) == 2:
                        cconf["name"] = cconf[1]
                # Allocate a name if not already assigned
                if "name" not in cconf:
                    cconf["name"] = node.get_next_intf_name()
                nconns.append(cconf)
            nconf["connections"] = nconns

        for name, node in self.hosts.items():
            nconf = node.config
            if "connections" not in nconf:
                continue
            for cconf in nconf["connections"]:
                # Eventually can add support for unconnected intf here.
                if "to" not in cconf:
                    continue
                to = cconf["to"]
                if to in self.switches:
                    switch = self.switches[to]
                    swconf = find_matching_net_config(name, cconf, switch.config)
                    self.add_native_link(switch, node, swconf, cconf)
                elif cconf["name"] not in node.intfs:
                    # Only add the p2p interface if not already there.
                    other = self.hosts[to]
                    oconf = find_matching_net_config(name, cconf, other.config)
                    self.add_native_link(node, other, cconf, oconf)

    @property
    def autonumber(self):
        return self.topoconf.get("networks-autonumber", False)

    @autonumber.setter
    def autonumber(self, value):
        self.topoconf["networks-autonumber"] = bool(value)

    def add_native_link(self, node1, node2, c1=None, c2=None):
        """Add a link between switch and node or 2 nodes."""
        isp2p = False

        c1 = {} if c1 is None else c1
        c2 = {} if c2 is None else c2

        if node1.name in self.switches:
            assert node2.name in self.hosts
        elif node2.name in self.switches:
            assert node1.name in self.hosts
            node1, node2 = node2, node1
            c1, c2 = c2, c1
        else:
            # p2p link
            assert node1.name in self.hosts
            assert node1.name in self.hosts
            isp2p = True

        if "name" not in c1:
            c1["name"] = node1.get_next_intf_name()
        if1 = c1["name"]

        if "name" not in c2:
            c2["name"] = node2.get_next_intf_name()
        if2 = c2["name"]

        super().add_link(node1, node2, if1, if2)

        if isp2p:
            node1.set_p2p_addr(node2, c1, c2)
        else:
            node2.set_lan_addr(node1, c2)

        node1.set_intf_constraints(if1, **c1)
        node2.set_intf_constraints(if2, **c2)

    def add_l3_node(self, name, config=None, **kwargs):
        """Add a node to munet."""

        if config and config.get("image"):
            cls = L3ContainerNode
        else:
            cls = L3Node
        return super().add_host(name, cls=cls, unet=self, config=config, **kwargs)

    def add_network(self, name, config=None, **kwargs):
        """Add a l2 or l3 switch to munet."""
        if config is None:
            config = {}

        cls = L3Bridge if config.get("ip") else L2Bridge
        return super().add_switch(name, cls=cls, config=config, **kwargs)

    async def run(self):
        tasks = []

        run_nodes = [x for x in self.hosts.values() if hasattr(x, "run_cmd")]
        run_nodes = [
            x for x in run_nodes if x.config.get("cmd") or x.config.get("image")
        ]

        if not self.pytest_config:
            pcapopt = ""
        else:
            pcapopt = self.pytest_config.getoption("--pcap")
            pcapopt = pcapopt if pcapopt else ""
        if pcapopt == "all":
            pcapopt = self.switches.keys()
        if pcapopt:
            for pcap in pcapopt.split(","):
                self.run_in_window(
                    f"tshark -s 1508 -i {pcap} -P -w capture-{pcap}.pcap",
                    background=True,
                    title=f"cap:{pcap}",
                )

        await asyncio.gather(*[x.run_cmd() for x in run_nodes])
        for node in run_nodes:
            task = asyncio.create_task(node.cmd_p.wait(), name=f"Node-{node.name}-cmd")
            task.add_done_callback(node.cmd_completed)
            tasks.append(task)
        return tasks

    async def async_delete(self):
        from munet.testing.util import async_pause_test  # pylint: disable=C0415

        if type(self) == Munet:  # pylint: disable=C0123
            self.logger.info("%s: deleting.", self)
        else:
            self.logger.debug("%s: Munet sub-class munet deleting.", self)

        if not self.pytest_config:
            pause = False
        else:
            pause = bool(self.pytest_config.getoption("--pause-at-end"))
            pause = pause or bool(self.pytest_config.getoption("--pause"))
        if pause:
            await async_pause_test("Before MUNET delete")

        await super().async_delete()


async def run_cmd_update_ceos(node, shell_cmd, cmds, cmd):
    cmd = cmd.strip()
    if shell_cmd or cmd != "/sbin/init":
        return cmds, cmd

    #
    # Add flash dir and mount it
    #
    flashdir = os.path.join(node.rundir, "flash")
    node.cmd_raises_host(f"mkdir -p {flashdir} && chmod 775 {flashdir}")
    cmds += [f"--volume={flashdir}:/mnt/flash"]

    #
    # Startup config (if not present already)
    #
    if startup_config := node.config.get("startup-config", None):
        dest = os.path.join(flashdir, "startup-config")
        if os.path.exists(dest):
            node.logger.info("Skipping copy of startup-config, already present")
        else:
            source = os.path.join(node.unet.config_dirname, startup_config)
            node.cmd_raises_host(f"cp {source} {dest} && chmod 664 {dest}")

    #
    # system mac address (if not present already
    #
    dest = os.path.join(flashdir, "system_mac_address")
    if os.path.exists(dest):
        node.logger.info("Skipping system-mac generation, already present")
    else:
        random_arista_mac = "00:1c:73:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        system_mac = node.config.get("system-mac", random_arista_mac)
        with open(dest, "w", encoding="ascii") as f:
            f.write(system_mac + "\n")
        node.cmd_raises_host(f"chmod 664 {dest}")

    args = []

    # Pass special args for the environment variables
    if "env" in node.config:
        args += [f"systemd.setenv={k}={v}" for k, v in node.config["env"].items()]

    return cmds, [cmd] + args


kind_run_cmd_update = {"ceos": run_cmd_update_ceos}
