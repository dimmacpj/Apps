import pyvisa

class HiokiPW:

    #Constructor
    def __init__(self):
        self.rm = pyvisa.ResourceManager()

    #Get resource list
    def getResource(self):
        return self.rm.list_resources()

    #Open port
    def open(self, resource):    
        try:
            self.pw = self.rm.open_resource(resource)
            self.pw.write_termination = '\r\n'
            self.pw.read_termination = '\r\n'
        except Exception as e:
            print(f'\n Open error: {e}')
    
    #Send Command
    def write(self, command):
        try:
            self.pw.write(command)
        except Exception as e:
            print(f'\n Command error: {e}')

    #Send query
    def query(self, command):
        try:
            response = self.pw.query(command)
        except Exception as e:
            print(f'\n Query error: {e}')
        
        return response

    #Close port
    def closeHio(self):
        try:
            self.pw.close()
        except Exception as e:
            print(f'\n Close error: {e}')