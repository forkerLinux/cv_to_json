#! /usr/bin/env python
# coding:utf-8

import re
from bs4 import BeautifulSoup
from bs4 import NavigableString

with open('cv.html', 'r') as f:
    content = f.read()


def get_cv():
    soup = BeautifulSoup(content, 'lxml')

    #############################################  基本信息
    basic_info = soup.select('.summary')[0].contents

    # 姓名
    name = soup.select('.summary > h1')[0].text


    gender_tuple = ('男', '女')
    marital_tuple = ('未婚', '已婚', '保密')
    work_status = '工作经验'
    email_status = '@'
    current_status = '现居住于'
    birthday_status = '月'
    phone_status = ''


    gender = ''
    marital_status = ''
    work_years = ''
    current_area = ''
    birthday = ''
    email = ''

    for item in basic_info:
        # 性别
        for gen in gender_tuple:
            if gen in item:
                gender = item.strip()

        # 婚姻状态
        for marital in marital_tuple:
            if marital in item:
                marital_status = item.strip()

        # 工作经验
        if work_status in item:
            work_years = item.strip()

        # 现居住地
        if current_status in item:
            current_area = item.strip()

        # 生日
        if birthday_status in item:
            birthday = item.strip()

        # email
        if email_status in str(item):
            email = item.a.text

        # phonenum
        if not isinstance(item,NavigableString) and len(item.text) == 11:
            phonenum = item.text

    basic = {
        'work_years': work_years,
        'birthday': birthday,
        'name': name,
        'current_area': current_area,
        'marital_status': marital_status,
        'gender': gender,
        'education': '',
        'phonenum': phonenum,
        'email': email,
        'avatar': '',
    }

    ############################################  详细信息
    details = soup.select('.details > dt')
    extra_list = [
        '兴趣爱好',
        '获得荣誉',
        '专业组织',
        '著作/论文',
        '专利',
        '宗教信仰',
        '特长职业目标',
        '特殊技能',
        '社会活动',
        '荣誉',
        '推荐信'
    ]
    extra_str = ''
    edu_extra_list = []

    for item in details:
        head = item.text.strip()
        ############################################## 求职意向
        if head == '求职意向':
            intension_info = item.next_sibling.find_all('li')
            status = intension_info[5].text.split('：')[1]
            area = intension_info[3].text.split('：')[1]
            title = intension_info[1].text.split('：')[1]
            trade = intension_info[2].text.split('：')[1]
            except_salary = intension_info[4].text.split('：')[1]

            intension = {
                'status': status,
                'area': area,
                'title': title,
                'trade': trade,
                'except_salary': except_salary
            }

        ############################################## 工作经历
        if head == '工作经历':
            work_experiences = item.next_sibling.select('.work-experience')

            career = []
            for exp in work_experiences:
                company = exp.h6.text.split('|')[0]
                title = exp.h6.text.split('|')[1]
                trade = exp.find(text=re.compile('行业类别')).strip().split('：')[1]
                area = ''
                start_time = exp.p.text.strip().split('--')[0].strip()
                end_time = exp.p.text.strip().split('--')[1].strip()
                duty = exp.find(text=re.compile('工作描述')).parent.next_sibling.next_sibling.strip()
                career_dict = {
                    'company': company,
                    'title': title,
                    'trade': trade,
                    'area': '',
                    'start_time': start_time,
                    'end_time': end_time,
                    'duty': duty
                }
                career.append(career_dict)

        ############################################## 教育经历
        if head == '教育经历':
            education_backgrounds = item.next_sibling.select('.education-background')

            education = []
            for edu in education_backgrounds:
                edu_info = edu.h6.text.strip().split('|')
                school = edu_info[0].strip()
                major = edu_info[1].strip()
                degree = edu_info[2].strip()
                edu_extra_list.append(degree)
                start_time = edu.p.text.strip().split('--')[0].strip()
                end_time = edu.p.text.strip().split('--')[1].strip()

                edu_dict = {
                    'school': school,
                    'major': major,
                    'degree': degree,
                    'start_time': start_time,
                    'end_time': end_time
                }

                education.append(edu_dict)
        ############################################  项目经验
        if head == '项目经验':
            project_experience = item.next_sibling.select('.project-experience')

            experience = []
            for pro in project_experience:
                project_name = pro.h6.text.strip()
                title = ''
                start_time = pro.p.text.strip().split('--')[0].strip()
                end_time = pro.p.text.strip().split('--')[1].strip()
                description = pro.find(text=re.compile('项目简介')).parent.next_sibling.next_sibling.strip()

                experience_dict = {
                    'project_name': project_name,
                    'title': title,
                    'description': description,
                    'start_time': start_time,
                    'end_time': end_time
                }

                experience.append(experience_dict)
        ############################################# 自我评价
        if head == '自我评价':
            description = item.next_sibling.text.strip()

        ############################################# 专业技能
        if head == '专业技能':
            professional_skill = item.parent.select('.professional-skill')

            tags = []

            for skill in professional_skill:
                tag = skill.text.strip().split('|')[0].strip()
                tags.append(tag)

        ############################################# 其他信息
        if head in extra_list:
            extra_title = head
            extra_content =  item.next_sibling.text.strip()
            extra_str += head + '\n' + extra_content + '\n'

    extra_str = extra_str[:-1]

    edu_list = ['其他', '初中', '中技', '高中', '中专', '大专', '本科', '硕士', 'MBA', 'EMBA', '博士']

    index_list = []
    for cu_edu in edu_extra_list:
        index_list.append(edu_list.index(cu_edu))
    basic['education'] = edu_list[max(index_list)]

    # 最终dict
    user_cv = {
        'basic': basic,
        'education': education,
        'experience': experience,
        'extra': extra_str,
        'career': career,
        'description': description,
        'tags': tags,
        'intension': intension
    }

    return user_cv


if __name__ == '__main__':
    cv = get_cv()
    print(cv)
