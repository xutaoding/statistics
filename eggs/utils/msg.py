from copy import copy


class FailureMsg(object):
    msg_error = {
        # Arguments type or length error
        105: {
            'status': '200',
            'error': 'argument format or length error: {info}'
        },

        # Arguments size error
        205: {
            'status': '200',
            'error': 'argument order error: {info}'
        },

    }

    def get_error_msg(self, error_type=None, info=None):
        error_msg = copy(self.msg_error.get(error_type, {}))
        if error_msg:
            error_msg['error'] = error_msg['error'].format(info=info)
        return error_msg

