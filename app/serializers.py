from flask_restful import fields

item_serializer = {

    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean

}


bucketlist_serializer = {
    'id': fields.Integer,
    'name': fields.String,
    'items': fields.Nested(item_serializer),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.Integer
}
