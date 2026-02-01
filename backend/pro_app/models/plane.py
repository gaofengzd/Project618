from pro_app.extensions.db import db
import json


class Plane(db.Model):
    __tablename__ = 'planes'
    id = db.Column(db.Integer, primary_key=True)  # 数据库主键
    reg_number = db.Column(db.String(20), unique=True)  # 对应前端 id (B-1234)
    flight_no = db.Column(db.String(20))  # 航班号
    model = db.Column(db.String(20))  # 机型
    status = db.Column(db.String(5))  # 状态 (H/M/G)
    route_from = db.Column(db.String(10))  # 起飞地
    route_to = db.Column(db.String(10))  # 目的地
    flight_time = db.Column(db.String(30))  # 时间

    # 转字典方法 (方便 jsonify)
    def to_dict(self):
        return {
            "id": self.reg_number,  # 前端用 id 代表 B-1234
            "flightNo": self.flight_no,
            "model": self.model,
            "status": self.status,
            "routeFrom": self.route_from,
            "routeTo": self.route_to,
            "time": self.flight_time
        }


class FaultRecord(db.Model):
    __tablename__ = 'fault_records'
    id = db.Column(db.Integer, primary_key=True)
    plane_id = db.Column(db.String(20))  # B-1234
    flight_no = db.Column(db.String(20))  # XXX2535
    fault_name = db.Column(db.String(50))  # 故障名称
    occur_time = db.Column(db.String(30))  # 发生时间 2026-01-08 15:15
    unit = db.Column(db.String(10))  # 单位

    # 为了列表页展示，我们需要简单的状态描述
    # (实际项目中这些应该由数据计算得出，这里为了简化直接存字符串)
    takeoff_status = db.Column(db.String(50))  # e.g. "温度异常(>80°C)"
    landing_status = db.Column(db.String(50))  # e.g. "正常"

    # 图表配置
    chart1_title = db.Column(db.String(100))
    threshold1 = db.Column(db.Float)
    chart2_title = db.Column(db.String(100))
    threshold2 = db.Column(db.Float)

    # 核心数据：MySQL没有原生数组类型，我们存为 JSON 字符串 (Text类型)
    takeoff_data_str = db.Column(db.Text)
    descent_data_str = db.Column(db.Text)

    def to_dict(self, detail=False):
        """
        detail=False: 列表页用，不返回庞大的图表数据
        detail=True: 详情页用，返回完整数据
        """
        base = {
            "planeId": self.plane_id,
            "flightNo": self.flight_no,
            "fault": self.fault_name,  # 前端列表页叫 fault, 详情页叫 faultName
            "faultName": self.fault_name,
            "date": self.occur_time,
            "unit": self.unit,
            "takeoffStatus": self.takeoff_status,
            "landingStatus": self.landing_status,
        }
        if detail:
            # 详情页需要把 JSON 字符串转回 数组
            base.update({
                "hasData": True,
                "chart1Title": self.chart1_title,
                "threshold1": self.threshold1,
                "takeoffData": json.loads(self.takeoff_data_str) if self.takeoff_data_str else [],
                "chart2Title": self.chart2_title,
                "threshold2": self.threshold2,
                "descentData": json.loads(self.descent_data_str) if self.descent_data_str else [],
            })
        return base