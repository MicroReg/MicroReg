from server.RegistryServer import RegistryServer
import os

microreg_path = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    os.environ['MICROREG_DATA_DIR'] = os.path.join(microreg_path, 'data_dir')
    s = RegistryServer('0.0.0.0', 8000, 1)
