from flask import redirect, render_template, request, url_for, flash
from models_mysql import course_news_orm, notifications_orm
from routes import common
import time
from tools import date_converter

def make_routes(fullstack_blueprint):
    @fullstack_blueprint.route('/notifications')
    def notifications():
        user = common.get_user_from_token()
        if user == None:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        user_notifications = notifications_orm.Notifications.get_all_notifications_by_receiver_id(user['id'])
        for notification in user_notifications:
            notification['jalali_date'] = date_converter.Date_converter.unix_timestamp_to_jalali(notification['unix_datetime'])
        unread_notifications_count = notifications_orm.Notifications.get_unread_notifications_count_by_receiver_id(user['id'])[0]
        return render_template('notifications.html', user=user, user_notifications=user_notifications, unread_notifications_count=unread_notifications_count)

    @fullstack_blueprint.route('/notifications/notification_<notification_id>')
    def notification_info(notification_id):
        user = common.get_user_from_token()
        if user == None:
            flash('کاربر گرامی، لطفا ابتدا ثبت نام یا ورود کنید.', 'danger')
            return redirect('/')
        else:
            user_full_name = user['full_name']
        user_notifications = notifications_orm.Notifications.get_all_notifications_by_receiver_id(user['id'])
        update_notification = notifications_orm.Notifications.update_notification(id = notification_id, is_read=notifications_orm.Notifications.Read_status.read) 
        notification = notifications_orm.Notifications.get_notification_by_id_and_user_id(user['id'], notification_id)
        if notification == None:
            flash(f'{user_full_name} گرامی پیامی برای نمایش وجود ندارد.', 'danger')
            return redirect('/notifications')
        notification['jalali_date'] = date_converter.Date_converter.unix_timestamp_to_jalali(notification['unix_datetime'])
        unread_notifications_count = notifications_orm.Notifications.get_unread_notifications_count_by_receiver_id(user['id'])[0]
        return render_template('notifications.html', user=user, notification=notification, user_notifications=user_notifications, unread_notifications_count=unread_notifications_count)