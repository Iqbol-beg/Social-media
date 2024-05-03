from rest_framework import serializers
from .models import User, Post,Followers,Comment, Like
from rest_framework.validators import ValidationError



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',  'password']


class RegisterSerializer(serializers.ModelSerializer):
    # username=serializers.CharField(required=True,   min_length=4)
    # password=serializers.CharField(required=True,   min_length=4, write_only=True)
    # confirm_password=serializers.CharField(required=True,   min_length=4, write_only=True)
    class Meta:
        model=User
        fields=['username', 'password']
    
    # def validate(self, attrs):
    #     confirm_password = attrs.get('confirm_password')
    #     password = attrs.get('password')
    #     username = attrs.get('username')

    #     if confirm_password != password:
    #             data={  
    #             'status': False,
    #             'message': "Password dont match",
    #                     }
    #             raise ValidationError(data)
            

    #     if not username.isalpha():
    #         data={
    #             'status': True,
    #             'message': "usernam faqat harflardan iborat bolsin",
    #                     }
    #         raise ValidationError(data)
    #     return attrs
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CreatePostSerialzer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = ['user', 'content']


class ReadPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'content', 'user',)

class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('content',)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = '__all__'

class FollowSerializer(serializers.Serializer):
    to_user_id = serializers.IntegerField()

    def validate_to_user_id(self, value):
        try:
            to_user =User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Foydalanuvchi topilmadi")
        return to_user

    def validate(self, attrs):
        user = self.context['request'].user
        to_user = attrs['to_user_id']

        if user == to_user:
            raise serializers.ValidationError("O'zingizga follow qila olmaysiz")

        if Followers.objects.filter(from_user=user, to_user=to_user).exists():
            raise serializers.ValidationError("Follow yuborib bolingan")

        return attrs

class AcceptFollowRequestSerializer(serializers.ModelSerializer):
    from_user_id = serializers.IntegerField()

    def validate_from_user_id(self, value):
        try:
            from_user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Foydalanuvchi topilmadi")
        return from_user

    def validate(self, attrs):
        user = self.context['request'].user
        from_user = attrs['from_user_id']

        if user == from_user:
            raise serializers.ValidationError("O'zingizga follow qila olmaysiz")

        relation = Followers.objects.filter(from_user=from_user, to_user=user).first()
        if not relation:
            raise serializers.ValidationError("Follow topilmadi")

        return attrs

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields ='__all__'
        

class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'comment'] 

    def validate(self, attrs):
        user = attrs.get('user')
        comment = attrs.get('comment')

        if not user:
            data={
                'status': False,
                'message': "Foydalanuvchi kerak",
                        }
            raise serializers.ValidationError(data)
        
        if not comment:
            data={
                'status': False,
                'message': "Sharh kiritilishi shart",
                        }
            raise serializers.ValidationError(data)

        return attrs
    

class AddLikeSerializer(serializers.ModelSerializer):
    class Meta:
        models = Like
        fields = ['user', 'post']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, data):
        user = data['User']
        post = data['post']
        existing_likes = Like.objects.filter(User=user, post=post)
        if existing_likes.exists():
            raise serializers.ValidationError("Bu foydalanuvchi allaqachon bu postni yoqtirgan")
        return data