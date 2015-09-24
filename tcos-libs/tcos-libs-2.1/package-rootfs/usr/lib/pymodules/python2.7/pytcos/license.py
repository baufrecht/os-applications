import datetime
import pickle

from Crypto.Cipher import AES
from Crypto import Random

from notification import Notify
try:
    import pytcos.tcos as tcos
except:
    pass


class License:
    '''gets the values (from the UI) and provide methods to alter the
       the license file
    '''
    def __init__(self, ui_dict=dict(), master_key=None, iv=None):
        if master_key and iv:
            self._master_key = master_key
            self._iv = iv
        else:
            self._master_key, self._iv = self.load_keys(f='key.dat')

        self.lic = dict(creation_date=datetime.date.today(),
                        expiration_date=None,
                        checksum=0)
        # get the configured values and merge them
        self.lic.update(ui_dict)
        # calculate expiration time
        if self.lic.get('usage_time'):
            self.lic['expiration_date'] = self.update_date(self.lic)
        else:
            # without an expiration_date, set it to a very far future ;-)
            self.lic['expiration_date'] = datetime.date(year=datetime.MAXYEAR,
                                                        month=12,
                                                        day=31)
        # calculate checksum
        self.lic['checksum'] = self.checksum_lic(self.lic)

    def load_keys(self, f):
        d = dict()
        try:
            fobj = open(f, 'rb')
            content = fobj.read()
            fobj.close()
            d = pickle.loads(content)
        except IOError as e:
            print("{} -> Using random data".format(e))
            d['master_key'] = Random.get_random_bytes(24)
            d['iv'] = Random.get_random_bytes(16)
        return (d['master_key'], d['iv'])


    def update_date(self, d):
        date_multi, date_unit = d['usage_time'][:-1], d['usage_time'][-1:]
        if date_unit == "y":
            days = 365 * int(date_multi)
        elif date_unit == "m":
            days = 30.42 * int(date_multi)
        elif date_unit == "d":
            days = int(date_multi)
        else:
            raise TypeError("{}: is an unknown unit".format(date_unit))
        return d['creation_date'] + datetime.timedelta(days=days)

    def checksum_lic(self, d):
        check_string = ''
        for k in d.keys():
            if k == 'checksum':
                continue
            try:
                check_string += str(d[k])
            except TypeError as e:
                print("{} has no str representation. {}".format(d[k], e))
        return sum(map(ord, check_string))

    def _get_aes_obj(self, master_key=None, iv=None):
        # IV vector is changing after encryption / decryption each block.
        # http://goo.gl/FHR9pC
        if not master_key:
            master_key = self._master_key
        if not iv:
            iv = self._iv
        return AES.new(master_key, AES.MODE_CBC, iv)

    def encrypt(self, data, chunk_size=16):
        aes = self._get_aes_obj()
        # In case the chunk is less than chunk_size, we pad it before
        # encrypting it.
        if isinstance(data, str):
            pad = " "
        else:
            pad = b"\0"
        if len(data) % chunk_size != 0:
            data += pad * ((chunk_size - len(data)) % chunk_size)
        return aes.encrypt(data)

    def decrypt(self, data):
        aes = self._get_aes_obj()
        return aes.decrypt(data)

    def serialize_dict(self, d):
        '''returns a py2 compatible serialized dict'''
        return pickle.dumps(d, protocol=2)

    def deserialize_obj(self, obj):
        '''returns a python dict from a serialized object'''
        return pickle.loads(obj)

    def write_lic(self, d, filename):
        file = open(filename, 'wb')
        if d.get('checksum'):
            file.write(self.encrypt(self.serialize_dict(d)))
            file.close()
            return True
        else:
            return False

    def load_lic(self, filename):
        file = open(filename, 'rb')
        content = file.read()
        file.close()
        try:
            return self.deserialize_obj(self.decrypt(content))
        except:
            raise

class Validator(License):

    def __init__(self, master_key, iv, schema_values):
        License.__init__(self, master_key=master_key, iv=iv)

        self.Validationtype = dict(VALID={'id': 0, 'text': 'valid'},
                                   EXPIRED={'id':1, 'text': "expired"},
                                   NOT_VALID={'id': 2, 'text': "Is not valid"},
                                   EMPTY={'id': 3, 'text': "Doesn't exist."})

        path_lic = schema_values.get('License.File', '')

        # no Licence is configured or part of the schema
        if not path_lic:
            self.Validationstatus = self.Validationtype['EMPTY']
        else:
            try:
                self.lic = self.load_lic('/tcos/link/licenses/'+path_lic)
            except:
                # means, there must have been an error while decoding, deserialization
                # wrong key?
                self.Validationstatus = self.Validationtype['NOT_VALID']

    def check(self):
        # job is already done
        try:
            return self.Validationstatus
        except:
            # we need to check for creation_date, expiration_date and checksum
            today = datetime.date.today()
            # creation date is in the future
            if self.lic['creation_date'] > today:
                return self.Validationtype['NOT_VALID']
            # expiration date is in the past
            if self.lic['expiration_date'] < today:
                return self.Validationtype['EXPIRED']
            # checksum is wrong, might be due to some manipulations
            if self.lic['checksum'] != self.checksum_lic(self.lic):
                return self.Validationtype['NOT_VALID']
            else:
                return self.Validationtype['VALID']

    # this is the very first method to enforce licensing, yet this one is quite simple and inflexible, so
    # more to come :-)
    def simple_notify(self):
        status = self.check()

        if status['id'] != 0:
            n = Notify()
            l = tcos.Logger()
            if status['id'] == 1:

                n.notify(text=r"License for {} has expired. {}".format(self.lic['package_name'],
                                                                      self.lic['expiration_date']))
            else:
                n.notify(text=r"License issue. {}".format(status['text']))
        else:
            pass


if __name__ == '__main__':
    pass
