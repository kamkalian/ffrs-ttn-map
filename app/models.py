from app import db


class Message(db.Model):

    msg_id = db.Column(db.Integer(), primary_key=True)

    app_id = db.Column(db.String(255))

    port = db.Column(db.Integer())
    counter = db.Column(db.Integer())
    payload_raw = db.Column(db.String(1000))
    altitude = db.Column(db.Integer())
    hdop = db.Column(db.Float())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    sats = db.Column(db.Integer())
    time = db.Column(db.DateTime())
    frequency = db.Column(db.Float())
    modulation = db.Column(db.String(64))
    data_rate = db.Column(db.String(64))
    airtime = db.Column(db.Integer())
    coding_rate = db.Column(db.String(64))

    dev_id = db.Column(db.String(80), db.ForeignKey('device.dev_id'))

    message_links = db.relationship('MessageLink', backref='message')


class MessageLink(db.Model):

    msg_link_id = db.Column(db.Integer(), primary_key=True)

    timestamp = db.Column(db.String(64))
    channel = db.Column(db.Integer())
    rssi = db.Column(db.Integer())
    snr = db.Column(db.Float())
    rf_chain = db.Column(db.Integer())

    msg_id = db.Column(db.Integer(), db.ForeignKey('message.msg_id'))

    gtw_id = db.Column(db.String(80), db.ForeignKey('gateway.gtw_id'))


class Device(db.Model):

    dev_id = db.Column(db.String(80), primary_key=True)

    hardware_serial = db.Column(db.String(255))

    messages = db.relationship('Message', backref='device')


class Gateway(db.Model):

    gtw_id = db.Column(db.String(80), primary_key=True)

    gtw_trusted = db.Column(db.Boolean())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    altitude = db.Column(db.Integer())

    message_links = db.relationship('MessageLink', backref='gateway')