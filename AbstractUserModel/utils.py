from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import uuid

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))

token_generator = AppTokenGenerator()

def generate_ref_code():
    code = uuid.uuid4().hex[:6].upper()
    return code

# def ranking(ambassador):
#     curr_rank = ambassador.rank
#     curr_count = ambassador.count
#     list_user = MyUser.objects.filter(is_superuser=False).order_by('count')
#     for i in list_user:
#         if i.count < curr_count:
#             i.rank = i.rank + 1
#         else:  
#             curr_rank = i.rank - 1
#             break
#     return curr_rank