from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'author_id' , 'created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']  # Make these fields read-only

    def create(self, validated_data):
        # Automatically set the user who created the author
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Ensure only the owner can update the author
        if instance.user != self.context['request'].user:
            raise serializers.ValidationError("You do not have permission to edit this author.")
        return super().update(instance, validated_data)
