from math import log2

from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

EXP_DIFF = 12


class UserSerializer(serializers.ModelSerializer):
    lvl_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'lvl_info'
        ]

    def get_lvl_info(self, obj):
        exp = 36
        lvl = int(log2(exp / EXP_DIFF + 1))
        exp_now = exp - EXP_DIFF * (2 ** (lvl - 1)) if lvl else exp
        exp_next = EXP_DIFF * (2 ** lvl) - exp_now

        return {
            'lvl': lvl,
            'exp_now': exp_now,
            'exp_next': exp_next,
            'exp': exp
        }
