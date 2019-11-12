from django.db import models



# 年龄段
class age(models.Model):
    age_section=models.CharField(max_length=225)
# 位置表
class position(models.Model):
    Position_type=models.CharField(max_length=225)
# 性别表
class sex(models.Model):
    sex_option=models.CharField(max_length=225)
# 演员个数
class actor_number(models.Model):
    actor_numbers=models.CharField(max_length=225)
# 产品类型
class product_option(models.Model):
    product_options=models.CharField(max_length=225)
# 内容类型
class content(models.Model):
    content_type=models.CharField(max_length=225)
# 剧本类型
class  script_type(models.Model):
    script_types=models.CharField(max_length=225)



# 剧本表
class play(models.Model):
    script_title=models.CharField(max_length=225)
    script_content=models.TextField()
    upload_time=models.DateTimeField(auto_now_add=True)
    author=models.CharField(max_length=225)
    Script_usage=models.IntegerField(default=0)
    play_age=models.ForeignKey(age,on_delete=models.CASCADE)
    play_position=models.ForeignKey(position,on_delete=models.CASCADE)
    play_sex=models.ForeignKey(sex,on_delete=models.CASCADE)
    play_actor_number=models.ForeignKey(actor_number,on_delete=models.CASCADE)
    play_product_option=models.ForeignKey(product_option,on_delete=models.CASCADE)
    play_content=models.ForeignKey(content,on_delete=models.CASCADE)
    play_script_type=models.ForeignKey(script_type,on_delete=models.CASCADE)

# script_title script_content upload_time author Script_usage play_age.age_section play_position.Position_type play_sex.sex_option
# play_actor_number.actor_numbers play_product_option.product_options play_content.content_type  play_script_type.script_types
