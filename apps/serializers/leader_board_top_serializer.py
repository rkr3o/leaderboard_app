from rest_framework import serializers
from constants.constants_and_methods import raise_error


class LeaderboardTopSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        # No input data expected for GET, so just return empty dict
        return {}

    def to_representation(self, instance):
        # instance will be list of dicts representing leaderboard entries
        return instance
