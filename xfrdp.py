import configparser
import locale
import os
import sys


class HelpCall(Exception):
    pass


class App:
    arguments: dict[str, str]
    key_list: list[str] = ['-s', '-h', '-n', '-p']
    install_path = os.path.join('etc', 'profile.d')
    config_path = os.path.join(install_path, 'xfrdp.ini')
    script_path = os.path.join(install_path, 'xfrdp.sh')
    

    def __init__(self):
        pass

    def set_args(self, args: list[str]):
        args = args
        try:
            self.__check_syntax(args)
        except (SyntaxError, HelpCall) as e:
            print('\n'.join((str(e), self.__str__())))
        else:
            self.__install_script(args)

    def __check_syntax(self, args: list[str]):
        for arg in args:
            if '-h' in args or len(args) == 1:
                raise HelpCall('HELP')
            elif not arg.startswith('-') or ':' not in arg or arg.split(':')[0] not in self.key_list:
                raise SyntaxError('Error: Unexpected keys')
    
    def __write_line(self, path: str, string: str):
        with open(path, 'w+') as cfg:
            cfg.write(string)

    def __install_script(self, args: list[str]):
        self.__write_line(self.script_path, '#!/bin/bash\n\n')
        self.__write_line(self.config_path, '[global]\n')

        for arg in args:
            key, value = arg.split(':')
            
            if key == '-s':
                self.__write_line(self.config_path, f'XRDPSRV={value}\n')
            elif key == '-n':
                self.__write_line(self.config_path, f'XUSER={value}\n')
            elif key == '-p':
                self.__write_line(self.config_path, f'XPWD={value}\n')

        config = configparser.ConfigParser()
        config.read(self.config_path)
        SERVER: str = config['global']['XRDPSRV']
        USERNAME: str = config['global']['XUSER']
        PASSWORD: str = config['global']['XPWD']
        
        os.system('apt update && apt -y upgrade && apt -y install freerdp2-x11 && apt -y install neovim')

        self.__write_line(self.script_path, f"xfreerdp -toggle-fullscreen /sound:format:1 /microphone:format:1 /cert:tofu /v:'{SERVER}' /u:'{USERNAME}' /p:'{PASSWORD}' /f /video || gnome-session-quit --logout --force")

        print('DONE!')

    def __str__(self):
        hlpru = 'Запускать только с правами рута.\n' \
                'Пример:\n' \
                '$ su \\ python3 xfrdp -s:192.168.1.4 -n:UserName -p:Password -a:yes\n' \
                '$ sudo python3 xfrdp -s:192.168.1.4 -n:UserName -p:Password -a:yes\n' \
                '\n' \
                '-s - Установить ip адрес удаленного рабочего стола.\n' \
                '-n - Установить имя пользователя удаленного рабочего стола.\n' \
                '-p - Установить пароль пользователя удаленного рабочего стола.\n' \
                '(ctrl+shift+f3 для использования терминала)\n'

        hlpen = 'Run only with root permissions.\n' \
                'Example:\n' \
                '$ su \\ python3 xfrdp -s:192.168.1.4 -n:UserName -p:Password -a:yes\n' \
                '$ sudo python3 xfrdp -s:192.168.1.4 -n:UserName -p:Password -a:yes\n' \
                '\n' \
                '-s - set rdp server ip.\n' \
                '-n - set username for rdp server.\n' \
                '-p - set user password for rdp server.\n' \
                '(ctrl+shift+f3 for using terminal)\n'
        
        if locale.getlocale()[0] == 'ru_RU':
            return hlpru
        else:
            return hlpen


def main():
    app = App()
    app.set_args(sys.argv)


if __name__ == "__main__":
    main()