from flask import Blueprint
from pro_app.extensions.db import db
from werkzeug.security import generate_password_hash
from .user import User
from .plane import Plane, FaultRecord
import json


init_bp = Blueprint('init_db', __name__)

# === 工具路由: 创建管理员账号 (仅用于初始化) ===
@init_bp.route('/init_db', methods=['GET'])
def init_data():
    db.create_all()

    # 1. 初始化管理员
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password_hash=generate_password_hash('123456'), role='管理员')
        db.session.add(admin)
        return "已添加管理员"

    # 2. 初始化飞机数据 (如果表是空的)
    if Plane.query.count() == 0:
        sample_planes = [
            Plane(reg_number='B-1234', flight_no='XXX2535', model='A320', status='H', route_from='LHD', route_to='LAX',
                  flight_time='2023-07-20 09:22'),
            Plane(reg_number='B-1235', flight_no='XXX3863', model='A320', status='M', route_from='CAN', route_to='HGH',
                  flight_time='2023-07-14 12:36'),
            Plane(reg_number='B-1236', flight_no='XXX405', model='A320', status='G', route_from='SZX', route_to='FRA',
                  flight_time='2023-02-06 17:33'),
            Plane(reg_number='B-1237', flight_no='XXX406', model='A320', status='G', route_from='SZX', route_to='FRA',
                  flight_time='2023-02-06 17:33'),
            Plane(reg_number='B-1238', flight_no='XXX407', model='B737', status='G', route_from='PEK', route_to='SHA',
                  flight_time='2023-02-06 18:00'),
            Plane(reg_number='B-9999', flight_no='XXX888', model='B737', status='M', route_from='CTU', route_to='XIY',
                  flight_time='2023-02-07 10:00'),
        ]
        db.session.add_all(sample_planes)
        db.session.commit()
        return "已添加6架样机数据"

    if FaultRecord.query.count() > 0:
        return "故障数据已存在"

        # 这里的 raw_data 就是你题目中提供的 JSON
    raw_data = [
        {
            "planeId": 'B-1234', "flightNo": 'XXX2535', "faultName": '压缩机出口温度过高', "date": '2026-01-08 15:15',
            "unit": '℃', "takeoffStatus": "温度异常(>80°C)", "landingStatus": "压力波动",
            "chart1Title": '异常参数趋势 (温度异常 > 80℃)', "threshold1": 70,
            "takeoffData": [25, 26, 26, 58, 80, 85, 90, 95, 86, 88, 85, 80],
            "chart2Title": '异常参数趋势 (温度波动)', "threshold2": 70,
            "descentData": [60, 62, 58, 55, 80, 48, 85, 42, 96, 38, 86, 30]
        },
        {
            "planeId": 'B-1234', "flightNo": 'XXX2535', "faultName": '转速超阈值', "date": '2026-01-08 15:15',
            "unit": 'RPM', "takeoffStatus": "转速偏高", "landingStatus": "正常",
            "chart1Title": '引擎转速监测', "threshold1": 9000,
            "takeoffData": [8000, 8100, 9500, 9600, 8500, 8200, 8000, 8000, 8000, 8000, 8000, 8000],
            "chart2Title": '转速波动', "threshold2": 9000,
            "descentData": [5000, 4000, 3000, 2000, 1000, 800, 0, 0, 0, 0, 0, 0]
        },
        {
            "planeId": 'B-1236', "flightNo": 'XXX405', "faultName": '环境管道漏气', "date": '2026-02-01 16:20',
            "unit": 'PSI', "takeoffStatus": "正常", "landingStatus": "压力异常",
            "chart1Title": '管道压力监测', "threshold1": 40,
            "takeoffData": [35, 35, 36, 35, 34, 35, 35, 36, 35, 34, 35, 35],
            "chart2Title": '压力异常骤降', "threshold2": 20,
            "descentData": [35, 34, 30, 25, 15, 10, 8, 5, 5, 4, 2, 0]
        }
    ]

    records = []
    for item in raw_data:
        rec = FaultRecord(
            plane_id=item['planeId'],
            flight_no=item['flightNo'],
            fault_name=item['faultName'],
            occur_time=item['date'],
            unit=item['unit'],
            takeoff_status=item['takeoffStatus'],
            landing_status=item['landingStatus'],
            chart1_title=item['chart1Title'],
            threshold1=item['threshold1'],
            chart2_title=item['chart2Title'],
            threshold2=item['threshold2'],
            # 关键：数组转 JSON 字符串
            takeoff_data_str=json.dumps(item['takeoffData']),
            descent_data_str=json.dumps(item['descentData'])
        )
        records.append(rec)

    db.session.add_all(records)
    db.session.commit()
    return "故障数据初始化完成"