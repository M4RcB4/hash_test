import base64
import hashlib

class CodecHelper:
    '''
    Can be used to build test data expectations
    '''

    @staticmethod
    def get_b64_sha512hash_1(text):
        '''
        text(utf8-EN)->(b64)->(SHA512)
        '''
        return hashlib.sha512(base64.b64encode(
            text.encode('utf-8'))).hexdigest()

    @staticmethod
    def get_b64_sha512hash_2(text):
        '''
        text(utf-8)->(b64)->(SHA512)->(b64)
        '''
        return base64.b64encode(hashlib.sha512(
            base64.b64encode(text.encode('utf-8')))
            .hexdigest().encode('utf-8'))
