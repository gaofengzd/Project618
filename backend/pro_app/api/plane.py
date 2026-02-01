from flask import Blueprint, jsonify, request
from pro_app.models.plane import Plane, FaultRecord


plane_bp = Blueprint('plane', __name__)

@plane_bp.route('/plane/plane_message', methods=['GET'])
def get_fleet():
    planes = Plane.query.all()
    # 将数据库对象列表转换为字典列表
    plane_list = [p.to_dict() for p in planes]
    return jsonify({
        'code': 200,
        'msg': '获取成功',
        'data': plane_list
    })


@plane_bp.route('/plane/faults/search', methods=['POST'])
def search_faults():
    data = request.get_json() or {}

    plane_id = data.get('planeId', '').strip()
    fault_name = data.get('faultName', '').strip()
    date_range = data.get('dateRange', [])  # ['2026-01-01', '2026-02-01']

    # 开始构建查询
    query = FaultRecord.query

    if plane_id:
        query = query.filter(FaultRecord.plane_id.ilike(f"%{plane_id}%"))
    if fault_name:
        query = query.filter(FaultRecord.fault_name.ilike(f"%{fault_name}%"))
    if date_range and len(date_range) == 2:
        # 简单的字符串比较 (前提是格式标准 YYYY-MM-DD)
        start_date = date_range[0] + " 00:00:00"
        end_date = date_range[1] + " 23:59:59"
        query = query.filter(FaultRecord.occur_time.between(start_date, end_date))

    records = query.all()
    # 列表页不需要详细的 array 数据，所以 to_dict(detail=False)
    return jsonify({'code': 200, 'data': [r.to_dict(detail=False) for r in records]})


# [新增] 2. 故障详情接口 (通过 飞机号+时间+故障名 唯一锁定)
@plane_bp.route('/plane/faults/detail', methods=['POST'])
def get_fault_detail():
    data = request.get_json()
    plane_id = data.get('planeId')
    date = data.get('date')
    fault = data.get('fault')

    record = FaultRecord.query.filter_by(
        plane_id=plane_id,
        occur_time=date,
        fault_name=fault
    ).first()

    if record:
        return jsonify({'code': 200, 'data': record.to_dict(detail=True)})
    else:
        return jsonify({'code': 404, 'msg': '未找到该记录'}), 404