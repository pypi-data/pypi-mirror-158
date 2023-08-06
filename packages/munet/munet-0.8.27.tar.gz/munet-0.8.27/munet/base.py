# -*- coding: utf-8 eval: (blacken-mode 1) -*-
#
# July 9 2021, Christian Hopps <chopps@labn.net>
#
# Copyright 2021, LabN Consulting, L.L.C.
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
"""A module that implements core functionality for library or standalone use."""
import asyncio
import datetime
import logging
import os
import re
import readline
import shlex
import signal
import subprocess
import sys
import tempfile
import time as time_mod

from munet import unshare


try:
    import pexpect

    from pexpect.popen_spawn import PopenSpawn
    from pexpect.replwrap import PEXPECT_CONTINUATION_PROMPT
    from pexpect.replwrap import PEXPECT_PROMPT
    from pexpect.replwrap import REPLWrapper

    have_repl_wrapper = True
except ImportError:
    have_repl_wrapper = False


root_hostname = subprocess.check_output("hostname")

# This allows us to cleanup any leftovers later on
os.environ["MUNET_PID"] = str(os.getpid())


class Timeout:
    """An object to passively monitor for timeouts."""

    def __init__(self, delta):
        self.started_on = datetime.datetime.now()
        self.expires_on = self.started_on + datetime.timedelta(seconds=delta)

    def elapsed(self):
        elapsed = datetime.datetime.now() - self.started_on
        return elapsed.total_seconds()

    def is_expired(self):
        return datetime.datetime.now() > self.expires_on


def shell_quote(command):
    """Return command wrapped in single quotes."""
    if sys.version_info[0] >= 3:
        return shlex.quote(command)
    return "'" + command.replace("'", "'\"'\"'") + "'"


def cmd_error(rc, o, e):
    s = f"rc {rc}"
    o = "\n\tstdout: " + o.strip() if o and o.strip() else ""
    e = "\n\tstderr: " + e.strip() if e and e.strip() else ""
    return s + o + e


def proc_error(p, o, e):
    if hasattr(p, "args"):
        args = p.args if isinstance(p.args, str) else " ".join(p.args)
    else:
        args = ""
    s = f"rc {p.returncode} pid {p.pid}\n\targs: {args}"
    o = "\n\tstdout: " + o.strip() if o and o.strip() else ""
    e = "\n\tstderr: " + e.strip() if e and e.strip() else ""
    return s + o + e


def comm_error(p):
    rc = p.poll()
    assert rc is not None
    if not hasattr(p, "saved_output"):
        p.saved_output = p.communicate()
    return proc_error(p, *p.saved_output)


async def acomm_error(p):
    rc = p.returncode
    assert rc is not None
    if not hasattr(p, "saved_output"):
        p.saved_output = await p.communicate()
    return proc_error(p, *p.saved_output)


def get_kernel_version():
    kvs = (
        subprocess.check_output("uname -r", shell=True, text=True).strip().split("-", 1)
    )
    kv = kvs[0].split(".")
    kv = [int(x) for x in kv]
    return kv


def convert_number(value) -> int:
    """Convert a number value with a possible suffix to an integer.

    >>> convert_number("100k") == 100 * 1024
    True
    >>> convert_number("100M") == 100 * 1000 * 1000
    True
    >>> convert_number("100Gi") == 100 * 1024 * 1024 * 1024
    True
    >>> convert_number("55") == 55
    True
    """
    if value is None:
        raise ValueError("Invalid value None for convert_number")
    rate = str(value)
    base = 1000
    if rate[-1] == "i":
        base = 1024
        rate = rate[:-1]
    suffix = "KMGTPEZY"
    index = suffix.find(rate[-1])
    if index == -1:
        base = 1024
        index = suffix.lower().find(rate[-1])
    if index != -1:
        rate = rate[:-1]
    return int(rate) * base ** (index + 1)


def get_tc_bits_value(user_value):
    value = convert_number(user_value) / 1000
    return f"{value:03f}kbit"


def get_tc_bytes_value(user_value):
    # Raw numbers are bytes in tc
    return convert_number(user_value)


def get_tmp_dir(uniq):
    return os.path.join(tempfile.mkdtemp(), uniq)


async def _async_get_exec_path(binary, cmdf, cache):
    if isinstance(binary, str):
        bins = [binary]
    else:
        bins = binary
    for b in bins:
        if b in cache:
            return cache[b]

        rc, output, _ = await cmdf("which " + b, warn=False)
        if not rc:
            cache[b] = os.path.abspath(output.strip())
            return cache[b]
    return None


def _get_exec_path(binary, cmdf, cache):
    if isinstance(binary, str):
        bins = [binary]
    else:
        bins = binary
    for b in bins:
        if b in cache:
            return cache[b]

        rc, output, _ = cmdf("which " + b, warn=False)
        if not rc:
            cache[b] = os.path.abspath(output.strip())
            return cache[b]
    return None


class Commander:  # pylint: disable=R0904
    """
    Commander.

    An object that can execute commands.
    """

    tmux_wait_gen = 0

    def __init__(self, name, logger=None, **kwargs):
        """Create a Commander."""
        del kwargs  # deal with lint warning
        self.name = name
        self.last = None
        self.exec_paths = {}
        self.pre_cmd = []
        self.pre_cmd_str = ""

        if not logger:
            self.logger = logging.getLogger(__name__ + ".commander." + name)
        else:
            self.logger = logger

        super().__init__()

    @property
    def is_container(self):
        return False

    def set_logger(self, logfile):
        self.logger = logging.getLogger(__name__ + ".commander." + self.name)
        if isinstance(logfile, str):
            handler = logging.FileHandler(logfile, mode="w")
        else:
            handler = logging.StreamHandler(logfile)

        fmtstr = "%(asctime)s.%(msecs)03d %(levelname)s: {}({}): %(message)s".format(
            self.__class__.__name__, self.name
        )
        handler.setFormatter(logging.Formatter(fmt=fmtstr))
        self.logger.addHandler(handler)

    def set_pre_cmd(self, pre_cmd=None):
        if not pre_cmd:
            self.pre_cmd = []
            self.pre_cmd_str = ""
        else:
            self.pre_cmd = pre_cmd
            self.pre_cmd_str = " ".join(self.pre_cmd) + " "

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"

    async def async_get_exec_path(self, binary):
        """Return the full path to the binary executable.

        `binary` :: binary name or list of binary names
        """
        return await _async_get_exec_path(
            binary, self.async_cmd_status_host, self.exec_paths
        )

    def get_exec_path(self, binary):
        """Return the full path to the binary executable.

        `binary` :: binary name or list of binary names
        """
        return _get_exec_path(binary, self.cmd_status_host, self.exec_paths)

    def get_exec_path_host(self, binary):
        """Return the full path to the binary executable.

        If the object is actually a derived class (e.g., a container) this method will
        return the exec path for the native namespace rather than the container. The
        path is the one which the other xxx_host methods will use.

        `binary` :: binary name or list of binary names
        """
        return get_exec_path_host(binary)

    def test(self, flags, arg):
        """Run test binary, with flags and arg"""
        test_path = self.get_exec_path(["test"])
        rc, _, _ = self.cmd_status([test_path, flags, arg], warn=False)
        return not rc

    def test_host(self, flags, arg):
        """Run test binary, with flags and arg"""
        test_path = self.get_exec_path(["test"])
        rc, _, _ = self.cmd_status_host([test_path, flags, arg], warn=False)
        return not rc

    def path_exists(self, path):
        """Check if path exists."""
        return self.test("-e", path)

    def get_cmd_container(self, cmd, sudo=False, tty=False):
        # The overrides of this function *do* use the self parameter
        del tty  # lint
        if sudo:
            return "sudo " + cmd
        return cmd

    def _get_cmd_str(self, cmd):
        if isinstance(cmd, str):
            return self.pre_cmd_str + cmd
        cmd = self.pre_cmd + cmd
        return " ".join(cmd)

    def _get_sub_args(self, cmd, defaults, **kwargs):
        if isinstance(cmd, str):
            defaults["shell"] = True
            pre_cmd = self.pre_cmd_str
        else:
            defaults["shell"] = False
            pre_cmd = self.pre_cmd
            cmd = [str(x) for x in cmd]

        env = {**(kwargs["env"] if "env" in kwargs else os.environ)}
        if "MUNET_NODENAME" not in env:
            env["MUNET_NODENAME"] = self.name
        kwargs["env"] = env

        defaults.update(kwargs)

        return pre_cmd, cmd, defaults

    def _popen_prologue(self, async_exec, method, cmd, skip_pre_cmd, **kwargs):
        if not async_exec:
            defaults = {
                "encoding": "utf-8",
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
            }
        else:
            defaults = {
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
            }
        pre_cmd, cmd, defaults = self._get_sub_args(cmd, defaults, **kwargs)
        self.logger.debug('%s: %s("%s", kwargs: %.80s)', self, method, cmd, defaults)
        actual_cmd = cmd if skip_pre_cmd else pre_cmd + cmd
        return actual_cmd, defaults

    async def _async_popen(self, method, cmd, skip_pre_cmd=False, **kwargs):
        acmd, kwargs = self._popen_prologue(True, method, cmd, skip_pre_cmd, **kwargs)
        p = await asyncio.create_subprocess_exec(*acmd, **kwargs)
        return p, acmd

    def _popen(self, method, cmd, skip_pre_cmd=False, **kwargs):
        acmd, kwargs = self._popen_prologue(False, method, cmd, skip_pre_cmd, **kwargs)
        p = subprocess.Popen(acmd, **kwargs)
        return p, acmd

    def _spawn(self, cmd, skip_pre_cmd=False, use_pty=False, **kwargs):
        pre_cmd, cmd, defaults = self._get_sub_args(cmd, {}, **kwargs)
        actual_cmd = cmd if skip_pre_cmd else pre_cmd + cmd
        if "shell" in defaults:
            del defaults["shell"]
        if "encoding" not in defaults:
            defaults["encoding"] = "utf-8"
            if "codec_errors" not in defaults:
                defaults["codec_errors"] = "ignore"

        defaults["env"]["PS1"] = "$ "

        # this is required to avoid receiving a STOPPED signal on expect!
        if not use_pty:
            defaults["preexec_fn"] = os.setsid

        self.logger.debug(
            '%s: _spawn("%s", skip_pre_cmd %s use_pty %s kwargs: %s)',
            self,
            cmd,
            skip_pre_cmd,
            use_pty,
            defaults,
        )

        # We don't specify a timeout it defaults to 30s is that OK?
        if not use_pty:
            p = PopenSpawn(actual_cmd, **defaults)
        else:
            p = pexpect.spawn(actual_cmd[0], actual_cmd[1:], **defaults)
        return p, actual_cmd

    def spawn(
        self,
        cmd,
        spawned_re,
        expects=(),
        sends=(),
        use_pty=False,
        logfile_read=None,
        logfile_send=None,
        trace=None,
        **kwargs,
    ):
        """
        Create a spawned send/expect process.

        Args:
            cmd - list of args to exec/popen with
            spawned_re - what to look for to know when done, `spawn` returns when seen
            expects - a list of regex other than `spawned_re` to look for. Commonly,
                "ogin:" or "[Pp]assword:"r.
            sends - what to send when an element of `expects` matches. So e.g., the
                username or password if thats what corresponding expect matched. Can
                be the empty string to send nothing.
            use_pty - true for pty based expect, otherwise uses popen (pipes/files)
            trace - if true then log send/expects
            **kwargs - kwargs passed on the _spawn.
        Returns:
            A pexpect process.
        Raises:
            pexpect.TIMEOUT, pexpect.EOF as documented in `pexpect`
            subprocess.CalledProcessError if EOF is seen and `cmd` exited then
                raises a CalledProcessError to indicate the failure.
        """
        p, ac = self._spawn(cmd, use_pty=use_pty, **kwargs)
        p.logfile_read = logfile_read
        p.logfile_send = logfile_send

        # for spawned shells (i.e., a direct command an not a console)
        # this is wrong and will cause 2 prompts
        if not use_pty:
            p.echo = False
            p.isalive = lambda: p.proc.poll() is None
            p.close = p.wait

        # Do a quick check to see if we got the prompt right away, otherwise we may be
        # at a console so we send a \n to re-issue the prompt
        self.logger.debug("%s: debug timeout STOPPED", self)
        index = p.expect([pexpect.TIMEOUT, pexpect.EOF], timeout=0.1)
        self.logger.debug("%s: got deubg quick index: '%s'", self, index)

        self.logger.debug("%s: quick check for spawned_re: %s", self, spawned_re)
        index = p.expect([spawned_re, pexpect.TIMEOUT, pexpect.EOF], timeout=0.1)
        if index == 0:
            assert p.match is not None
            self.logger.debug(
                "%s: got spawned_re quick: '%s' matching '%s'",
                self,
                p.match.group(0),
                spawned_re,
            )
            return p

        # Now send a CRLF to cause the prompt (or whatever else) to re-issue
        p.send("\n")
        try:
            patterns = [spawned_re, *expects]

            self.logger.debug("%s: expecting: %s", self, patterns)

            while index := p.expect(patterns):
                if trace:
                    assert p.match is not None
                    self.logger.debug(
                        "%s: got expect: '%s' matching %d '%s', sending '%s'",
                        self,
                        p.match.group(0),
                        index,
                        spawned_re,
                        sends[index - 1],
                    )
                if sends[index - 1]:
                    p.send(sends[index - 1])
            self.logger.debug(
                "%s: got spawned_re: '%s' matching '%s'",
                self,
                p.match.group(0),
                spawned_re,
            )
            return p
        except pexpect.TIMEOUT:
            self.logger.warning(
                "%s: TIMEOUT looking for spawned_re '%s' buffer: '%s'",
                self,
                spawned_re,
                p.buffer,
            )
            raise
        except pexpect.EOF as eoferr:
            if p.isalive():
                raise
            p.close()
            rc = p.status
            error = subprocess.CalledProcessError(rc, ac)
            p.expect(pexpect.EOF)
            error.stdout = p.before
            raise error from eoferr

    async def shell_spawn(
        self,
        cmd,
        prompt,
        expects=(),
        sends=(),
        noecho=False,
        use_pty=False,
        logfile_read=None,
        logfile_send=None,
        **kwargs,
    ):
        """
        Create a shell REPL (read-eval-print-loop).

        Args:
            cmd - shell and list of args to popen with
            prompt - the REPL prompt to look for, the function returns when seen
            expects - a list of regex other than `spawned_re` to look for. Commonly,
                "ogin:" or "[Pp]assword:"r.
            sends - what to send when an element of `expects` matches. So e.g., the
                username or password if thats what corresponding expect matched. Can
                be the empty string to send nothing.
            use_pty - true for pty based expect, otherwise uses popen (pipes/files)
            **kwargs - kwargs passed on the _spawn.
        """
        prompt = r"({}|{})".format(re.escape(PEXPECT_PROMPT), prompt)
        p = self.spawn(
            cmd, prompt, expects, sends, use_pty, logfile_read, logfile_send, **kwargs
        )

        ps1 = PEXPECT_PROMPT
        ps2 = PEXPECT_CONTINUATION_PROMPT

        # Avoid problems when =/usr/bin/env= prints the values
        ps1p = ps1[:5] + "${UNSET_V}" + ps1[5:]
        ps2p = ps2[:5] + "${UNSET_V}" + ps2[5:]

        pchg = "PS1='{0}' PS2='{1}' PROMPT_COMMAND=''\n".format(ps1p, ps2p)
        p.send(pchg)
        return ShellWrapper(
            p, ps1, None, extra_init_cmd="export PAGER=cat", noecho=noecho
        )

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
        return self._popen("popen", cmd, **kwargs)[0]

    def popen_host(self, cmd, **kwargs):
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
        return Commander._popen(self, "popen_host", cmd, **kwargs)[0]

    async def async_popen(self, cmd, **kwargs):
        """Creates a pipe with the given `command`.

        Args:
            cmd: `str` or `list` of command to open a pipe with.

            **kwargs: kwargs is eventually passed on to create_subprocess_exec. If
                `command` is a string then will be invoked with `bash -c`, otherwise
                `command` is a list and will be invoked without a shell.

        Returns:
            a asyncio.subprocess.Process object.
        """
        p, _ = await self._async_popen("async_popen", cmd, **kwargs)
        return p

    async def async_popen_host(self, cmd, **kwargs):
        """Creates a pipe with the given `command`.

        Args:
            cmd: `str` or `list` of command to open a pipe with.

            **kwargs: kwargs is eventually passed on to create_subprocess_exec. If
                `command` is a string then will be invoked with `bash -c`, otherwise
                `command` is a list and will be invoked without a shell.

        Returns:
            a asyncio.subprocess.Process object.
        """
        p, _ = await Commander._async_popen(self, "async_popen_host", cmd, **kwargs)
        return p

    @staticmethod
    def _cmd_status_input(stdin):
        pinput = None
        if isinstance(stdin, (bytes, str)):
            pinput = stdin
            stdin = subprocess.PIPE
        return pinput, stdin

    def _cmd_status_finish(self, p, c, ac, o, e, raises, warn):
        rc = p.returncode
        self.last = (rc, ac, c, o, e)
        if rc:
            if warn:
                self.logger.warning("%s: proc failed: %s:", self, proc_error(p, o, e))
            if raises:
                # error = Exception("stderr: {}".format(stderr))
                # This annoyingly doesnt' show stderr when printed normally
                error = subprocess.CalledProcessError(rc, ac)
                error.stdout, error.stderr = o, e
                raise error
        return rc, o, e

    def _cmd_status(self, cmds, raises=False, warn=True, stdin=None, **kwargs):
        """Execute a command."""
        pinput, stdin = Commander._cmd_status_input(stdin)
        p, actual_cmd = self._popen("cmd_status", cmds, stdin=stdin, **kwargs)
        o, e = p.communicate(pinput)
        return self._cmd_status_finish(p, cmds, actual_cmd, o, e, raises, warn)

    async def _async_cmd_status(
        self, cmds, raises=False, warn=True, stdin=None, text=None, **kwargs
    ):
        """Execute a command."""
        pinput, stdin = Commander._cmd_status_input(stdin)
        p, actual_cmd = await self._async_popen(
            "async_cmd_status", cmds, stdin=stdin, **kwargs
        )

        if text is False:
            encoding = None
        else:
            encoding = kwargs.get("encoding", "utf-8")

        if encoding is not None and isinstance(pinput, str):
            pinput = pinput.encode(encoding)
        o, e = await p.communicate(pinput)
        if encoding is not None:
            o = o.decode(encoding) if o is not None else o
            e = e.decode(encoding) if e is not None else e
        return self._cmd_status_finish(p, cmds, actual_cmd, o, e, raises, warn)

    def cmd_get_cmd_list(self, cmd):
        if not isinstance(cmd, str):
            cmds = cmd
        else:
            # Make sure the code doesn't think `cd` will work.
            assert not re.match(r"cd(\s*|\s+(\S+))$", cmd)
            cmds = ["/bin/bash", "-c", cmd]
        return cmds

    def cmd_status(self, cmd, **kwargs):
        "Run given command returning status and outputs"
        #
        # This method serves as the basis for all derived sync cmd variations, so to
        # override sync cmd behavior simply override this function and *not* the other
        # variations, unless you are changing only that variation's behavior
        #
        cmds = self.cmd_get_cmd_list(cmd)
        return self._cmd_status(cmds, **kwargs)

    def cmd_raises(self, cmd, **kwargs):
        """Execute a command. Raise an exception on errors"""

        _, stdout, _ = self.cmd_status(cmd, raises=True, **kwargs)
        return stdout

    def cmd_status_host(self, cmd, **kwargs):
        # Make sure the command runs on the host and not in any container.
        return Commander.cmd_status(self, cmd, **kwargs)

    def cmd_raises_host(self, cmd, **kwargs):
        # Make sure the command runs on the host and not in any container.
        return Commander.cmd_status(self, cmd, raises=True, **kwargs)

    async def async_cmd_status(self, cmd, **kwargs):
        #
        # This method serves as the basis for all derived async cmd variations, so to
        # override async cmd behavior simply override this function and *not* the other
        # variations, unless you are changing only that variation's behavior
        #
        cmds = self.cmd_get_cmd_list(cmd)
        return await self._async_cmd_status(cmds, **kwargs)

    async def async_cmd_raises(self, cmd, **kwargs):
        """Execute a command. Raise an exception on errors"""
        _, stdout, _ = await self.async_cmd_status(cmd, raises=True, **kwargs)
        return stdout

    async def async_cmd_status_host(self, cmd, **kwargs):
        # Make sure the command runs on the host and not in any container.
        return await Commander.async_cmd_status(self, cmd, **kwargs)

    async def async_cmd_raises_host(self, cmd, **kwargs):
        # Make sure the command runs on the host and not in any container.
        _, stdout, _ = await Commander.async_cmd_status(
            self, cmd, raises=True, **kwargs
        )
        return stdout

    def cmd_legacy(self, cmd, **kwargs):
        """Execute a command with stdout and stderr joined, *IGNORES ERROR*."""

        defaults = {"stderr": subprocess.STDOUT}
        defaults.update(kwargs)
        _, stdout, _ = self.cmd_status(cmd, raises=False, **defaults)
        return stdout

    # Run a command in a new window (gnome-terminal, screen, tmux, xterm)
    def run_in_window(
        self,
        cmd,
        wait_for=False,
        background=False,
        name=None,
        title=None,
        forcex=False,
        new_window=False,
        tmux_target=None,
        on_host=False,
    ):
        """
        Run a command in a new window (TMUX, Screen or XTerm).

        Args:
            wait_for: True to wait for exit from command or `str` as channel neme to
                      signal on exit, otherwise False
            background: Do not change focus to new window.
            title: Title for new pane (tmux) or window (xterm).
            name: Name of the new window (tmux)
            forcex: Force use of X11.
            new_window: Open new window (instead of pane) in TMUX
            tmux_target: Target for tmux pane.

        Returns:
            the pane/window identifier from TMUX (depends on `new_window`)
        """

        channel = None
        if isinstance(wait_for, str):
            channel = wait_for
        elif wait_for is True:
            channel = "{}-wait-{}".format(os.getpid(), Commander.tmux_wait_gen)
            Commander.tmux_wait_gen += 1

        sudo_path = get_exec_path_host(["sudo"])

        if not self.is_container or on_host:
            # This is the command to execute to be inside the namespace.
            # We are getting into trouble with quoting.
            cmd = f"/usr/bin/env MUNET_NODENAME={self.name} {cmd}"
            nscmd = sudo_path + " " + self.pre_cmd_str + cmd
        else:
            nscmd = self.get_cmd_container(cmd, sudo=True, tty=True)

        if "TMUX" in os.environ and not forcex:
            cmd = [get_exec_path_host("tmux")]
            if new_window:
                cmd.append("new-window")
                cmd.append("-P")
                if name:
                    cmd.append("-n")
                    cmd.append(name)
                if tmux_target:
                    cmd.append("-t")
                    cmd.append(tmux_target)
            else:
                cmd.append("split-window")
                cmd.append("-P")
                cmd.append("-h")
                if not tmux_target:
                    tmux_target = os.getenv("TMUX_PANE", "")
            if background:
                cmd.append("-d")
            if tmux_target:
                cmd.append("-t")
                cmd.append(tmux_target)
            if isinstance(nscmd, str) or title or channel:
                if not isinstance(nscmd, str):
                    nscmd = shlex.join(nscmd)
                if title:
                    nscmd = f"printf '\033]2;{title}\033\\'; {nscmd}"
                if channel:
                    nscmd = f'trap "tmux wait -S {channel}; exit 0" EXIT; {nscmd}'
                cmd.append(nscmd)
            else:
                cmd.extend(nscmd)
        elif "STY" in os.environ and not forcex:
            # wait for not supported in screen for now
            channel = None
            cmd = [get_exec_path_host("screen")]
            if not os.path.exists(
                "/run/screen/S-{}/{}".format(os.environ["USER"], os.environ["STY"])
            ):
                cmd = ["sudo", "-u", os.environ["SUDO_USER"]] + cmd
            cmd.append(nscmd)
        elif "DISPLAY" in os.environ:
            # We need it broken up for xterm
            user_cmd = cmd
            cmd = [get_exec_path_host("xterm")]
            if "SUDO_USER" in os.environ:
                cmd = [
                    get_exec_path_host("sudo"),
                    "-u",
                    os.environ["SUDO_USER"],
                ] + cmd
            if title:
                cmd.append("-T")
                cmd.append(title)
            cmd.append("-e")
            cmd.append(sudo_path)
            cmd.extend(self.pre_cmd)
            cmd.extend(["bash", "-c", user_cmd])
            # if channel:
            #    return self.cmd_raises(cmd, skip_pre_cmd=True)
            # else:
            p = self.popen(
                cmd,
                skip_pre_cmd=True,
                stdin=None,
                shell=False,
            )
            time_mod.sleep(2)
            if p.poll() is not None:
                self.logger.error("%s: Failed to launch xterm: %s", self, comm_error(p))
            return p
        else:
            self.logger.error(
                "DISPLAY, STY, and TMUX not in environment, can't open window"
            )
            raise Exception("Window requestd but TMUX, Screen and X11 not available")

        pane_info = self.cmd_raises(cmd, skip_pre_cmd=True).strip()

        # Re-adjust the layout
        if "TMUX" in os.environ:
            self.cmd_status(
                "tmux select-layout -t {} tiled".format(
                    pane_info if not tmux_target else tmux_target
                ),
                skip_pre_cmd=True,
            )

        # Wait here if we weren't handed the channel to wait for
        if channel and wait_for is True:
            cmd = [get_exec_path_host("tmux"), "wait", channel]
            self.cmd_status(cmd, skip_pre_cmd=True)

        return pane_info

    def delete(self):
        "Calls self.async_delete within an exec loop"
        asyncio.run(self.async_delete())

    async def async_delete(self):
        self.logger.info("%s: deleted", self)


class InterfaceMixin:
    """A mixin class to support interface functionality."""

    def __init__(self, **kwargs):
        del kwargs  # get rid of lint
        self.intf_addrs = {}
        self.net_intfs = {}
        self.next_intf_index = 0
        self.basename = "eth"
        # self.basename = name + "-eth"
        super().__init__()

    @property
    def intfs(self):
        return self.intf_addrs.keys()

    @property
    def networks(self):
        return self.net_intfs.keys()

    def net_addr(self, netname):
        if netname not in self.net_intfs:
            return None
        return self.intf_addrs[self.net_intfs[netname]]

    def set_intf_basename(self, basename):
        self.basename = basename

    def get_next_intf_name(self):
        while True:
            ifname = self.basename + str(self.next_intf_index)
            self.next_intf_index += 1
            if ifname not in self.intf_addrs:
                break
        return ifname

    def register_interface(self, ifname):
        if ifname not in self.intf_addrs:
            self.intf_addrs[ifname] = None

    def register_network(self, netname, ifname):
        if netname in self.net_intfs:
            assert self.net_intfs[netname] == ifname
        else:
            self.net_intfs[netname] = ifname

    def get_linux_tc_args(self, ifname, config):
        """Get interface constraints (jitter, delay, rate) for linux TC

        The keys and their values are as follows:

        delay :: (int) number of microseconds
        jitter :: (int) number of microseconds
        jitter-correlation :: (float) % correlation to previous (default 10%)
        loss :: (float) % of loss
        loss-correlation :: (float) % correlation to previous (default 25%)
        rate :: (int or str) bits per second, string allows for use of
                {KMGTKiMiGiTi} prefixes "i" means K == 1024 otherwise K == 1000
        """
        netem_args = ""

        def get_number(c, v, d=None):
            if v not in c or c[v] is None:
                return d
            return convert_number(c[v])

        delay = get_number(config, "delay")
        if delay is not None:
            netem_args += f" delay {delay}usec"

        jitter = get_number(config, "jitter")
        if jitter is not None:
            if not delay:
                raise ValueError("jitter but no delay specified")
            jitter_correlation = get_number(config, "jitter-correlation", 10)
            netem_args += f" {jitter}usec {jitter_correlation}%"

        loss = get_number(config, "loss")
        if loss is not None:
            if not delay:
                raise ValueError("loss but no delay specified")
            loss_correlation = get_number(config, "loss-correlation", 25)
            netem_args += f" loss {loss}% {loss_correlation}%"

        if (o_rate := config.get("rate")) is None:
            return netem_args, ""

        #
        # This comment is not correct, but is trying to talk through/learn the
        # machinery.
        #
        # tokens arrive at `rate` into token buffer.
        # limit - number of bytes that can be queued waiting for tokens
        #   -or-
        # latency - maximum amount of time a packet may sit in TBF queue
        #
        # So this just allows receiving faster than rate for latency amount of
        # time, before dropping.
        #
        # latency = sizeofbucket(limit) / rate (peakrate?)
        #
        #   32kbit
        # -------- = latency = 320ms
        #  100kbps
        #
        #  -but then-
        # burst ([token] buffer) the largest number of instantaneous
        # tokens available (i.e, bucket size).

        tbf_args = ""
        DEFLIMIT = 1518 * 1
        DEFBURST = 1518 * 2
        try:
            tc_rate = o_rate["rate"]
            tc_rate = convert_number(tc_rate)
            limit = convert_number(o_rate.get("limit", DEFLIMIT))
            burst = convert_number(o_rate.get("burst", DEFBURST))
        except (KeyError, TypeError):
            tc_rate = convert_number(o_rate)
            limit = convert_number(DEFLIMIT)
            burst = convert_number(DEFBURST)
        tbf_args += f" rate {tc_rate/1000}kbit"
        if delay:
            # give an extra 1/10 of buffer space to handle delay
            tbf_args += f" limit {limit} burst {burst}"
        else:
            tbf_args += f" limit {limit} burst {burst}"

        count = 1
        selector = f"root handle {count}:"
        if netem_args:
            self.cmd_raises(f"tc qdisc add dev {ifname} {selector} netem {netem_args}")
            count += 1
            selector = f"parent {count-1}: handle {count}"
        # Place rate limit after delay otherwise limit/burst too complex
        if tbf_args:
            self.cmd_raises(f"tc qdisc add dev {ifname} {selector} tbf {tbf_args}")

        self.cmd_raises(f"tc qdisc show dev {ifname}")

        return netem_args, tbf_args

    def set_intf_constraints(self, ifname, **constraints):
        """Set interface outbound constraints.

        Set outbound constraints (jitter, delay, rate) for an interface. All arguments
        may also be passed as a string and will be converted to numerical format. All
        arguments are also optional. If not specified then that existing constraint will
        be cleared.

        Args:
            delay (int): number of microseconds.
            jitter (int): number of microseconds.
            jitter-correlation (float): Percent correlation to previous (default 10%).
            loss (float): Percent of loss.
            loss-correlation (float): Percent correlation to previous (default 25%).
            rate (int): bits per second, string allows for use of
                {KMGTKiMiGiTi} prefixes "i" means K == 1024 otherwise K == 1000.
        """
        netem_args, tbf_args = self.get_linux_tc_args(ifname, constraints)
        count = 1
        selector = f"root handle {count}:"
        if netem_args:
            self.cmd_raises(f"tc qdisc add dev {ifname} {selector} netem {netem_args}")
            count += 1
            selector = f"parent {count-1}: handle {count}"
        # Place rate limit after delay otherwise limit/burst too complex
        if tbf_args:
            self.cmd_raises(f"tc qdisc add dev {ifname} {selector} tbf {tbf_args}")

        self.cmd_raises(f"tc qdisc show dev {ifname}")


class LinuxNamespace(Commander, InterfaceMixin):
    """
    A linux Namespace.

    An object that creates and executes commands in a linux namespace
    """

    def __init__(
        self,
        name,
        net=True,
        mount=True,
        uts=True,
        cgroup=False,
        ipc=False,
        pid=False,
        time=False,
        user=False,
        unshare_inline=False,
        unshare_func_test=None,
        set_hostname=True,
        private_mounts=None,
        logger=None,
    ):
        """
        Create a new linux namespace.

        Args:
            name: Internal name for the namespace.
            net: Create network namespace.
            mount: Create network namespace.
            uts: Create UTS (hostname) namespace.
            cgroup: Create cgroup namespace.
            ipc: Create IPC namespace.
            pid: Create PID namespace, also mounts new /proc.
            time: Create time namespace.
            user: Create user namespace, also keeps capabilities.
                set_hostname: Set the hostname to `name`, uts must also be True.
                private_mounts: List of strings of the form
                "[/external/path:]/internal/path. If no external path is specified a
                tmpfs is mounted on the internal path. Any paths specified are first
                passed to `mkdir -p`.
            logger: Passed to superclass.
        """
        super().__init__(name=name, logger=logger)

        self.logger.debug("%s: creating", self)

        self.cwd = os.path.abspath(os.getcwd())

        nslist = []
        # cmd = [] if os.geteuid() == 0 else ["/usr/bin/sudo"]
        cmd = []
        cmd += ["/usr/bin/unshare"]
        flags = ""
        self.a_flags = []
        self.ifnetns = {}
        self.uflags = 0
        self.p_ns_fds = None
        self.p_ns_fnames = None

        uflags = 0
        if cgroup:
            nslist.append("cgroup")
            flags += "C"
            uflags |= unshare.CLONE_NEWCGROUP
        if ipc:
            nslist.append("ipc")
            flags += "i"
            uflags |= unshare.CLONE_NEWIPC
        if mount:
            nslist.append("mnt")
            flags += "m"
            uflags |= unshare.CLONE_NEWNS
        if net:
            nslist.append("net")
            # if pid:
            #     os.system(f"touch /tmp/netns-{name}")
            #     cmd.append(f"--net=/tmp/netns-{name}")
            # else:
            flags += "n"
            uflags |= unshare.CLONE_NEWNET
        if pid:
            nslist.append("pid")
            flags += "f"
            flags += "p"
            cmd.append("--mount-proc")
            uflags |= unshare.CLONE_NEWPID
        if time:
            nslist.append("time")
            flags += "T"
            uflags |= unshare.CLONE_NEWTIME
        if user:
            nslist.append("user")
            flags += "U"
            cmd.append("--keep-caps")
            uflags |= unshare.CLONE_NEWUSER
        if uts:
            nslist.append("uts")
            flags += "u"
            uflags |= unshare.CLONE_NEWUTS

        if flags:
            if aflags := flags.replace("f", ""):
                self.a_flags = ["-" + x for x in aflags]
            cmd.extend(["-" + x for x in flags])
            # cmd.append(f"-{flags}")

        if pid:
            cmd.append(get_exec_path_host("tini"))
            cmd.append("-vvv")
        cmd.append("/bin/cat")

        self.ppid = os.getppid()
        if unshare_inline:
            if (
                unshare_func_test
                or sys.version_info[0] < 3
                or (sys.version_info[0] == 3 and sys.version_info[1] < 9)
            ):
                # get list of namespace file descriptors before we unshare
                self.p_ns_fds = []
                self.p_ns_fnames = []
                tmpflags = uflags
                for i in range(0, 64):
                    v = 1 << i
                    if (tmpflags & v) == 0:
                        continue
                    tmpflags &= ~v
                    if v in unshare.namespace_files:
                        path = os.path.join("/proc/self", unshare.namespace_files[v])
                        if os.path.exists(path):
                            self.p_ns_fds.append(os.open(path, 0))
                            self.p_ns_fnames.append(f"{path} -> {os.readlink(path)}")
                            self.logger.debug(
                                "%s: saving old namespace fd %s (%s)",
                                self,
                                self.p_ns_fnames[-1],
                                self.p_ns_fds[-1],
                            )
                    if not tmpflags:
                        break
            else:
                self.p_ns_fds = None
                self.p_ns_fnames = None
                self.ppid_fd = os.pidfd_open(self.ppid)  # pylint: disable=no-member

            self.logger.debug(
                "%s: unshare to new namespaces %s",
                self,
                unshare.clone_flag_string(uflags),
            )
            unshare.unshare(uflags)
            self.pid = os.getpid()
            self.uflags = uflags
            p = None
        else:
            # Using cat and a stdin PIPE is nice as it will exit when we do. However,
            # we also detach it from the pgid so that signals do not propagate to it.
            # This is b/c it would exit early (e.g., ^C) then, at least the main munet
            # proc which has no other processes like frr daemons running, will take the
            # main network namespace with it, which will remove the bridges and the
            # veth pair (because the bridge side veth is deleted).
            self.logger.debug("%s: creating namespace process: %s", self, cmd)
            p = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,  # detach from pgid so signals don't propogate
                shell=False,
            )
            self.pid = p.pid

        self.p = p
        self.logger.debug("%s: namespace pid: %d", self, self.pid)

        # -----------------------------------------------
        # Now let's wait until unshare completes it's job
        # -----------------------------------------------
        timeout = Timeout(30)
        while (p is None or p.poll() is None) and not timeout.is_expired():
            for fname in tuple(nslist):
                if p is None:
                    # self is changing so compare with parent pid's NS
                    pidnsf = os.readlink("/proc/{}/ns/{}".format(self.ppid, fname))
                else:
                    # new pid is changing so compare with self's NS
                    pidnsf = os.readlink("/proc/{}/ns/{}".format(self.pid, fname))
                selfnsf = os.readlink("/proc/self/ns/{}".format(fname))
                # See if their namespace is different and remove from check if so
                if selfnsf != pidnsf:
                    nslist.remove(fname)
            if not nslist or (pid and nslist == ["pid"]):
                break
            elapsed = int(timeout.elapsed())
            if elapsed <= 3:
                time_mod.sleep(0.1)
            elif elapsed > 10:
                self.logger.warning(
                    "%s: unshare taking more than %ss: %s", self, elapsed, nslist
                )
                time_mod.sleep(3)
            else:
                self.logger.info(
                    "%s: unshare taking more than %ss: %s", self, elapsed, nslist
                )
                time_mod.sleep(1)
        if p is not None:
            if p.poll():
                self.logger.error(
                    "%s: namespace process failed: %s", self, comm_error(p)
                )
            assert p.poll() is None, "unshare unexpectedly exited!"
        # assert not nslist, "unshare never unshared!"

        # Set pre-command based on our namespace proc
        self.base_pre_cmd = ["/usr/bin/nsenter", *self.a_flags, "-t", str(self.pid)]
        if not pid:
            self.base_pre_cmd.append("-F")
        self.set_pre_cmd(self.base_pre_cmd)

        # Remount /sys to pickup any changes, but keep root /sys/fs/cgroup
        # This pattern could be made generic and supported for any overlapping mounts
        tmpmnt = f"/tmp/cgm-{self.pid}"

        if self.p is None:
            self.cmd_raises("mount --make-rprivate /")

        #
        # We do not want cmd_status in child classes (e.g., container) for the remaining
        # setup calls in this __init__ function.
        #
        self.cmd_status_host(f"mkdir {tmpmnt} && mount --rbind /sys/fs/cgroup {tmpmnt}")
        self.cmd_status_host("mount -t sysfs sysfs /sys")
        self.cmd_status_host(f"mount --move {tmpmnt} /sys/fs/cgroup && rmdir {tmpmnt}")
        # self.cmd_raises(
        #     f"mount -N {self.pid} --bind /sys/fs/cgroup /sys/fs/cgroup",
        #     skip_pre_cmd=True,
        # )
        # o = self.cmd_raises("ls -l /sys/fs/cgroup")
        # self.logger.warning("XXX %s", o)

        # Set the hostname to the namespace name
        if uts and set_hostname and self.p is not None:
            # Debugging get the root hostname
            self.cmd_status_host("hostname " + self.name)
            nroot = subprocess.check_output("hostname")
            if root_hostname != nroot:
                result = self.p.poll()
                assert root_hostname == nroot, "STATE of namespace process {}".format(
                    result
                )

        if private_mounts:
            if isinstance(private_mounts, str):
                private_mounts = [private_mounts]
            for m in private_mounts:
                s = m.split(":", 1)
                if len(s) == 1:
                    self.tmpfs_mount(s[0])
                else:
                    self.bind_mount(s[0], s[1])

        o = self.cmd_status_host("ls -l /proc/{}/ns".format(self.pid))
        self.logger.debug("namespaces:\n %s", o)

        # will cache the path, which is important in delete to avoid running a shell
        # which can hang during cleanup
        self.ip_path = get_exec_path_host("ip")
        self.cmd_status_host([self.ip_path, "link", "set", "lo", "up"])

        self.logger.info("%s: created", self)

    def tmpfs_mount(self, inner):
        self.logger.debug("Mounting tmpfs on %s", inner)
        self.cmd_raises("mkdir -p " + inner)
        self.cmd_raises("mount -n -t tmpfs tmpfs " + inner)

    def bind_mount(self, outer, inner):
        self.logger.debug("Bind mounting %s on %s", outer, inner)
        if self.test_host("-f", outer):
            self.cmd_raises(f"mkdir -p {os.path.dirname(inner)} && touch {inner}")
        else:
            if not self.test_host("-e", outer):
                self.cmd_raises(f"mkdir -p {outer}")
            self.cmd_raises(f"mkdir -p {inner}")
        self.cmd_raises("mount --rbind {} {} ".format(outer, inner))

    def add_netns(self, ns):
        self.logger.debug("Adding network namespace %s", ns)

        if os.path.exists("/run/netns/{}".format(ns)):
            self.logger.warning("%s: Removing existing nsspace %s", self, ns)
            try:
                self.delete_netns(ns)
            except Exception as ex:
                self.logger.warning(
                    "%s: Couldn't remove existing nsspace %s: %s",
                    self,
                    ns,
                    str(ex),
                    exc_info=True,
                )
        self.cmd_raises_host([self.ip_path, "netns", "add", ns])

    def delete_netns(self, ns):
        self.logger.debug("Deleting network namespace %s", ns)
        self.cmd_raises_host([self.ip_path, "netns", "delete", ns])

    def set_intf_netns(self, intf, ns, up=False):
        # In case a user hard-codes 1 thinking it "resets"
        ns = str(ns)
        if ns == "1":
            ns = str(self.pid)

        self.logger.debug("Moving interface %s to namespace %s", intf, ns)

        cmd = [self.ip_path, "link", "set", intf, "netns", ns]
        if up:
            cmd.append("up")
        self.intf_ip_cmd(intf, cmd)
        if ns == str(self.pid):
            # If we are returning then remove from dict
            if intf in self.ifnetns:
                del self.ifnetns[intf]
        else:
            self.ifnetns[intf] = ns

    def reset_intf_netns(self, intf):
        self.logger.debug("Moving interface %s to default namespace", intf)
        self.set_intf_netns(intf, str(self.pid))

    def intf_ip_cmd(self, intf, cmd):
        """Run an ip command, considering an interface's possible namespace."""
        if intf in self.ifnetns:
            if isinstance(cmd, list):
                assert cmd[0].endswith("ip")
                cmd[1:1] = ["-n", self.ifnetns[intf]]
            else:
                assert cmd.startswith("ip ")
                cmd = "ip -n " + self.ifnetns[intf] + cmd[2:]
        self.cmd_raises_host(cmd)

    def intf_tc_cmd(self, intf, cmd):
        """Run a tc command, considering an interface's possible namespace."""
        if intf in self.ifnetns:
            if isinstance(cmd, list):
                assert cmd[0].endswith("tc")
                cmd[1:1] = ["-n", self.ifnetns[intf]]
            else:
                assert cmd.startswith("tc ")
                cmd = "tc -n " + self.ifnetns[intf] + cmd[2:]
        self.cmd_raises_host(cmd)

    def set_cwd(self, cwd):
        # Set pre-command based on our namespace proc
        if os.path.abspath(cwd) == os.path.abspath(os.getcwd()):
            self.set_pre_cmd(self.base_pre_cmd)
            return
        self.logger.debug("%s: new CWD %s", self, cwd)
        self.set_pre_cmd(self.base_pre_cmd + ["--wd=" + cwd])

    def cleanup_proc(self, p):
        if not p or p.returncode is not None:
            return None

        self.logger.debug("%s: terminate process: %s (%s)", self, p.pid, p)
        os.kill(-p.pid, signal.SIGTERM)
        try:
            assert isinstance(p, subprocess.Popen)
            p.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            self.logger.warning(
                "%s: terminate timeout, killing %s (%s)", self, p.pid, p
            )
            os.kill(-p.pid, signal.SIGKILL)
            try:
                assert isinstance(p, subprocess.Popen)
                p.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                self.logger.warning("%s: kill timeout", self)
                return p
            except Exception as error:
                self.logger.warning(
                    "%s: kill unexpected exception: %s", self, error, exc_info=True
                )
        except Exception as error:
            self.logger.warning(
                "%s: terminate unexpected exception: %s", self, error, exc_info=True
            )
        return None

    async def async_cleanup_proc(self, p):
        if not p or p.returncode is not None:
            return None

        self.logger.debug("%s: terminate process: %s (%s)", self, p.pid, p)

        # XXX Are we calling this -p.pid on cmd_p which isn't setup right for that?
        os.kill(-p.pid, signal.SIGTERM)
        try:
            assert not isinstance(p, subprocess.Popen)
            await asyncio.wait_for(p.communicate(), timeout=10)
        except asyncio.TimeoutError:
            self.logger.warning(
                "%s: terminate timeout, killing %s (%s)", self, p.pid, p
            )
            os.kill(-p.pid, signal.SIGKILL)
            try:
                assert not isinstance(p, subprocess.Popen)
                await asyncio.wait_for(p.communicate(), timeout=2)
            except asyncio.TimeoutError:
                self.logger.warning("%s: kill timeout", self)
                return p
            except Exception as error:
                self.logger.warning(
                    "%s: kill unexpected exception: %s", self, error, exc_info=True
                )
        except Exception as error:
            self.logger.warning(
                "%s: terminate unexpected exception: %s", self, error, exc_info=True
            )
        return None

    async def async_delete(self):
        if type(self) == LinuxNamespace:  # pylint: disable=C0123
            self.logger.info("%s: deleting", self)
        else:
            self.logger.debug("%s: LinuxNamespace sub-class deleting", self)

        if self.p is not None:
            self.cleanup_proc(self.p)
        # return to the previous namespace
        if self.uflags:
            # This only works in linux>=5.8
            if self.p_ns_fds is None:
                self.logger.debug(
                    "%s: restoring namespaces %s",
                    self,
                    unshare.clone_flag_string(self.uflags),
                )
                fd = unshare.pidfd_open(self.ppid)
                unshare.setns(fd, self.uflags)
                os.close(fd)
            else:
                while self.p_ns_fds:
                    fd = self.p_ns_fds.pop()
                    fname = self.p_ns_fnames.pop()
                    self.logger.debug(
                        "%s: restoring namespace from fd %s (%s)", self, fname, fd
                    )
                    retry = 3
                    for i in range(0, retry):
                        try:
                            unshare.setns(fd, 0)
                            break
                        except OSError as error:
                            self.logger.warning(
                                "%s: could not reset to old namespace fd %s (%s): %s",
                                self,
                                fname,
                                fd,
                                error,
                            )
                            if i == retry - 1:
                                raise
                        time_mod.sleep(1)
                    os.close(fd)
                self.p_ns_fds = None
                self.p_ns_fnames = None

        self.set_pre_cmd(["/bin/false"])

        await super().async_delete()


class SharedNamespace(Commander):
    """
    Share another namespace.

    An object that executes commands in an existing pid's linux namespace
    """

    def __init__(self, name, pid, aflags=("-a",), logger=None):
        """
        Share a linux namespace.

        Args:
            name: Internal name for the namespace.
            pid: PID of the process to share with.
        """
        super().__init__(name=name, logger=logger)

        self.logger.debug("%s: Creating", self)

        self.cwd = os.path.abspath(os.getcwd())
        self.pid = pid

        self.base_pre_cmd = ["/usr/bin/nsenter", *aflags, "-t", str(self.pid)]
        self.set_pre_cmd(self.base_pre_cmd)

        self.ip_path = self.get_exec_path("ip")

    def set_cwd(self, cwd):
        # Set pre-command based on our namespace proc
        if os.path.abspath(cwd) == os.path.abspath(os.getcwd()):
            self.set_pre_cmd(self.base_pre_cmd)
            return
        self.logger.debug("%s: new CWD %s", self, cwd)
        self.set_pre_cmd(self.base_pre_cmd + ["--wd=" + cwd])


class Bridge(SharedNamespace, InterfaceMixin):
    """
    A linux bridge.
    """

    next_ord = 1

    @classmethod
    def _get_next_id(cls):
        # Do not use `cls` here b/c that makes the variable class specific
        n = Bridge.next_ord
        Bridge.next_ord = n + 1
        return n

    def __init__(self, name=None, unet=None, logger=None, **kwargs):
        """Create a linux Bridge."""

        self.id = self._get_next_id()
        if not name:
            name = "br{}".format(self.id)
        super().__init__(
            name=name, pid=unet.pid, aflags=unet.a_flags, logger=logger, **kwargs
        )

        self.set_intf_basename(self.name + "-e")

        self.unet = unet

        self.logger.debug("Bridge: Creating")

        assert len(self.name) <= 16  # Make sure fits in IFNAMSIZE
        self.cmd_raises(f"ip link delete {name} || true")
        self.cmd_raises(f"ip link add {name} type bridge")
        self.cmd_raises(f"ip link set {name} up")

        self.logger.debug("%s: Created, Running", self)

    async def async_delete(self):
        """Stop the bridge (i.e., delete the linux resources)."""
        if type(self) == Bridge:  # pylint: disable=C0123
            self.logger.info("%s: deleting", self)
        else:
            self.logger.debug("%s: Bridge sub-class deleting", self)

        rc, o, e = await self.async_cmd_status(
            [self.ip_path, "link", "show", self.name],
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            warn=False,
        )
        if not rc:
            rc, o, e = await self.async_cmd_status(
                [self.ip_path, "link", "delete", self.name],
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                warn=False,
            )
        if rc:
            self.logger.error(
                "%s: error deleting bridge %s: %s",
                self,
                self.name,
                cmd_error(rc, o, e),
            )

        await super().async_delete()


class BaseMunet(LinuxNamespace):
    """
    Munet.
    """

    def __init__(self, isolated=True, **kwargs):
        """Create a Munet."""

        self.hosts = {}
        self.switches = {}
        self.links = {}
        self.macs = {}
        self.rmacs = {}
        self.isolated = isolated

        self.cli_server = None
        self.cli_sockpath = None
        self.cli_histfile = None
        self.cli_in_window_cmds = {}
        self.cli_run_cmds = {}

        super().__init__(name="munet", mount=True, net=isolated, uts=isolated, **kwargs)

        # this is for testing purposes do not use
        if not BaseMunet.g_unet:
            BaseMunet.g_unet = self

        self.logger.debug("%s: Creating", self)

    def __getitem__(self, key):
        if key in self.switches:
            return self.switches[key]
        return self.hosts[key]

    def add_host(self, name, cls=LinuxNamespace, **kwargs):
        """Add a host to munet."""

        self.logger.debug("%s: add_host %s(%s)", self, cls.__name__, name)

        self.hosts[name] = cls(name, **kwargs)

        # Create a new mounted FS for tracking nested network namespaces creatd by the
        # user with `ip netns add`

        # XXX why is this failing with podman???
        # self.hosts[name].tmpfs_mount("/run/netns")

        return self.hosts[name]

    def add_link(self, node1, node2, if1, if2, **intf_constraints):
        """Add a link between switch and node or 2 nodes.

        If constraints are given they are applied to each endpoint. See
        `InterfaceMixin::set_intf_constraints()` for more info.
        """
        isp2p = False

        try:
            name1 = node1.name
        except AttributeError:
            if node1 in self.switches:
                node1 = self.switches[node1]
            else:
                node1 = self.hosts[node1]
            name1 = node1.name

        try:
            name2 = node2.name
        except AttributeError:
            if node2 in self.switches:
                node2 = self.switches[node2]
            else:
                node2 = self.hosts[node2]
            name2 = node2.name

        if name1 in self.switches:
            assert name2 in self.hosts
        elif name2 in self.switches:
            assert name1 in self.hosts
            name1, name2 = name2, name1
            if1, if2 = if2, if1
        else:
            # p2p link
            assert name1 in self.hosts
            assert name2 in self.hosts
            isp2p = True

        lname = "{}:{}-{}:{}".format(name1, if1, name2, if2)
        self.logger.debug("%s: add_link %s%s", self, lname, " p2p" if isp2p else "")
        self.links[lname] = (name1, if1, name2, if2)

        # And create the veth now.
        if isp2p:
            lhost, rhost = self.hosts[name1], self.hosts[name2]
            lifname = "i1{:x}".format(lhost.pid)
            rifname = "i2{:x}".format(rhost.pid)
            self.cmd_raises_host(
                "ip link add {} type veth peer name {}".format(lifname, rifname)
            )

            self.cmd_raises_host("ip link set {} netns {}".format(lifname, lhost.pid))
            lhost.cmd_raises_host("ip link set {} name {}".format(lifname, if1))
            lhost.cmd_raises_host("ip link set {} up".format(if1))
            lhost.register_interface(if1)

            self.cmd_raises_host("ip link set {} netns {}".format(rifname, rhost.pid))
            rhost.cmd_raises_host("ip link set {} name {}".format(rifname, if2))
            rhost.cmd_raises_host("ip link set {} up".format(if2))
            rhost.register_interface(if2)
        else:
            switch = self.switches[name1]
            host = self.hosts[name2]
            lifname = "i1{:x}".format(switch.pid)
            rifname = "i1{:x}".format(host.pid)

            if len(if1) > 16:
                logging.error('"%s" len %s > 16', if1, len(if1))
            elif len(if2) > 16:
                logging.error('"%s" len %s > 16', if2, len(if2))
            assert len(if1) <= 16 and len(if2) <= 16  # Make sure fits in IFNAMSIZE

            self.logger.debug("%s: Creating veth pair for link %s", self, lname)
            self.cmd_raises_host(
                f"ip link add {lifname} type veth peer name {rifname} netns {host.pid}"
            )
            self.cmd_raises_host(f"ip link set {lifname} netns {switch.pid}")
            switch.cmd_raises_host(f"ip link set {lifname} name {if1}")
            host.cmd_raises_host(f"ip link set {rifname} name {if2}")

            switch.register_interface(if1)
            host.register_interface(if2)
            host.register_network(switch.name, if2)

            switch.cmd_raises_host(f"ip link set {if1} master {switch.name}")
            switch.cmd_raises_host(f"ip link set {if1} up")
            host.cmd_raises_host(f"ip link set {if2} up")

        # Cache the MAC values, and reverse mapping
        self.get_mac(name1, if1)
        self.get_mac(name2, if2)

        # Setup interface constraints if provided
        if intf_constraints:
            node1.set_intf_constraints(if1, **intf_constraints)
            node2.set_intf_constraints(if2, **intf_constraints)

    def add_switch(self, name, cls=Bridge, **kwargs):
        """Add a switch to munet."""

        self.logger.debug("%s: add_switch %s(%s)", self, cls.__name__, name)
        self.switches[name] = cls(name, unet=self, **kwargs)
        return self.switches[name]

    def get_mac(self, name, ifname):
        if name in self.hosts:
            dev = self.hosts[name]
        else:
            dev = self.switches[name]

        if (name, ifname) not in self.macs:
            _, output, _ = dev.cmd_status_host("ip -o link show " + ifname)
            m = re.match(".*link/(loopback|ether) ([0-9a-fA-F:]+) .*", output)
            mac = m.group(2)
            self.macs[(name, ifname)] = mac
            self.rmacs[mac] = (name, ifname)

        return self.macs[(name, ifname)]

    async def _delete_link(self, lname):
        rname, rif = self.links[lname][2:4]
        host = self.hosts[rname]

        self.logger.debug("%s: Deleting veth pair for link %s", self, lname)
        rc, o, e = await host.async_cmd_status_host(
            [self.ip_path, "link", "delete", rif],
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            warn=False,
        )
        if rc:
            self.logger.error(
                "Error deleting veth pair %s: %s", lname, cmd_error(rc, o, e)
            )

    def _delete_links(self):
        return asyncio.gather(*[self._delete_link(x) for x in self.links])

    async def async_delete(self):
        """Delete the munet topology."""
        if type(self) == BaseMunet:  # pylint: disable=C0123
            self.logger.info("%s: deleting.", self)
        else:
            self.logger.debug("%s: BaseMunet sub-class deleting.", self)

        try:
            await self._delete_links()
        except Exception as error:
            self.logger.error(
                "%s: error deleting links: %s", self, error, exc_info=True
            )
        try:
            # Delete hosts and switches, wait for them all to complete
            # even if there is an exception.
            htask = [x.async_delete() for x in self.hosts.values()]
            stask = [x.async_delete() for x in self.switches.values()]
            await asyncio.gather(*htask, *stask, return_exceptions=True)
        except Exception as error:
            self.logger.error(
                "%s: error deleting hosts and switches: %s", self, error, exc_info=True
            )

        self.links = {}
        self.hosts = {}
        self.switches = {}

        if self.cli_server:
            self.cli_server.cancel()
            self.cli_server = None
        if self.cli_sockpath:
            await self.async_cmd_status("rm -rf " + os.path.dirname(self.cli_sockpath))
            self.cli_sockpath = None
        if self.cli_histfile:
            readline.write_history_file(self.cli_histfile)
            self.cli_histfile = None

        await super().async_delete()


BaseMunet.g_unet = None


#
# Extra Functional REPLWrapper from pexpect
#
if have_repl_wrapper:

    class ShellWrapper(REPLWrapper):
        """
        REPLWrapper - a read-execute-print-loop interface
        """

        def __init__(
            self, cmd_or_spawn, orig_prompt, prompt_change, noecho=False, **kwargs
        ):
            self.noecho = noecho
            super().__init__(cmd_or_spawn, orig_prompt, prompt_change, **kwargs)

        def cmd_status(self, cmd, timeout=-1):
            """Execute a shell command

            Returns status and (strip/cleaned \r) output
            """
            output = self.run_command(cmd, timeout, async_=False)
            idx = output.find(cmd)
            if idx == -1:
                if not self.noecho:
                    logging.warning(
                        "Didn't find command ('%s') in expected output ('%s')",
                        cmd,
                        output,
                    )
            else:
                # Remove up to and including the command from the output stream
                output = output[idx + len(cmd) :].strip()

            scmd = "echo $?"
            rcstr = self.run_command(scmd)
            idx = rcstr.find(scmd)
            if idx == -1:
                if self.noecho:
                    logging.warning(
                        "Didn't find status ('%s') in expected output ('%s')",
                        scmd,
                        rcstr,
                    )
                try:
                    rc = int(rcstr)
                except Exception:
                    rc = 255
            else:
                rcstr = rcstr[idx + len(scmd) :].strip()
                rc = int(rcstr)
            return rc, output.replace("\r", "").strip()

        def cmd_raises(self, cmd, timeout=-1):
            """Execute a shell command.

            Returns (strip/cleaned \r) ouptut
            Raises CalledProcessError on non-zero exit status
            """
            rc, output = self.cmd_status(cmd, timeout)
            if rc:
                error = subprocess.CalledProcessError(rc, cmd)
                error.stdout = output
                raise error
            return output


# ---------------------------
# Root level utility function
# ---------------------------


def get_exec_path(binary):
    return commander.get_exec_path(binary)


def get_exec_path_host(binary):
    return commander.get_exec_path(binary)


commander = Commander("munet")
