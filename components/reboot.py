#   Copyright Peznauts <kevin@cloudnull.com>. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

from directord import components


class Component(components.ComponentBase):
    def __init__(self):
        super().__init__(desc="Process restart command")

    def args(self):
        """Set default arguments for a component."""

        super().args()
        self.parser.add_argument(
            "time",
            help="Reboot after %(default)s seconds.",
            default=10,
            type=int,
        )
        self.cacheable = False
        self.requires_lock = True

    def server(self, exec_array, data, arg_vars):
        """Return data from formatted cacheevict action.

        :param exec_array: Input array from action
        :type exec_array: List
        :param data: Formatted data hash
        :type data: Dictionary
        :param arg_vars: Pre-Formatted arguments
        :type arg_vars: Dictionary
        :returns: Dictionary
        """

        super().server(exec_array=exec_array, data=data, arg_vars=arg_vars)
        data["time"] = self.known_args.time
        return data

    def client(self, cache, job):
        """Run cache restart command operation.

        :param cache: Caching object used to template items within a command.
        :type cache: Object
        :param job: Information containing the original job specification.
        :type job: Dictionary
        :returns: tuple
        """

        commands = [
            "sleep {}".format(job["time"]),
            "systemctl --message='Directord reboot instruction' reboot",
        ]
        shell_commands = ";".join(commands)
        stdout, stderr, outcome = self.run_command(
            shell_commands, no_block=True
        )
        return stdout, stderr, outcome, shell_commands
