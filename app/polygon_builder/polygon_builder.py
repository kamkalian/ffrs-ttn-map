import requests
from app.models import Gateway, MessageLink, Message, Device, Polygon, Polygonpoint, Log
from flask import json
from app import db
from datetime import datetime, timedelta
from app.polygon_builder.Rangearea import Rangearea


def run_polygon_builder():
    '''
    Holt die Messages aus der Datenbank. 
    Anschließend wird die Analyse gestartet, bei der neue Polygone ermittelt werden
    '''

    # Heraus finden wann der letzte Lauf durchgeführt wurde
    last_log = Log.query.filter_by(modul='Polygon Builder', state='start').order_by(Log.timestamp.desc()).first()

    # alle Gatewas holen
    try:
        gateway_list = Gateway.query.all()
    except:
        print('Datenbank Fehler!')

    # Ein Rangearea Object anlegen
    range_area = Rangearea()

    # RSSI Bereiche definieren
    range_area.add_rssi_range(-99, 0, '#ff0000')
    range_area.add_rssi_range(-104, -100, '#FF7F00')
    range_area.add_rssi_range(-109, -105, '#ffff00')
    range_area.add_rssi_range(-114, -110, '#00ff00')
    range_area.add_rssi_range(-119, -115, '#00ffff')
    range_area.add_rssi_range(-200, -120, '#0000ff')

    # Liste für die Rangepoints erstellen
    range_point_list = []

    # Alle Gateways durchgehen
    for gateway in gateway_list:

        # print(gateway)

        # Gateway hinzufügen
        range_area.add_gateway(
            gateway.gtw_id,
            gateway.latitude,
            gateway.longitude)

        for message_link in gateway.message_links:

            # Wenn die Message kein datetime Object hat wird sie verworfen.
            if type(message_link.message.time) != datetime:
                continue
            
            # Messages die vor dem letzten Lauf empfangen wurden werden verworfen.
            if last_log != None:    
                diff_dt = last_log.timestamp - message_link.message.time
                diff = diff_dt.seconds + diff_dt.days * 24 * 3600
                # print(message_link.message.time, diff)
                if diff > 0:
                    continue

            range_point = Rangearea.range_point(
                message_link.message.latitude,
                message_link.message.longitude,
                message_link.message.altitude, 
                message_link.rssi,
                gateway.gtw_id)

            range_point_list.append(range_point)

    '''
    Da wir jetzt nur noch die zuletzt reingekommenden Punkte verarbeiten, müssen 
    die schon erstellenten Polygone mit in die Analyse einfließen.
    Dazu werden hier aus den Polygonen die Punkte extrahiert und daraus dann range_points gebaut.
    '''
    if len(range_point_list) > 20:

        # Log Eintrag hinzufügen
        current_dt = datetime.now()
        new_log = Log(modul='Polygon Builder', state='start', timestamp=current_dt.strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_log)
        db.session.commit()

        polygon_points = Polygonpoint.query.all()
        for pp in polygon_points:

            # Ein kleines Mapping zwichen RSSI und der fill_color
            rssi = None
            if pp.polygon.fill_color == '#ff0000':
                rssi = -50
            if pp.polygon.fill_color == '#FF7F00':
                rssi = -102
            if pp.polygon.fill_color == '#ffff00':
                rssi = -107
            if pp.polygon.fill_color == '#00ff00':
                rssi = -112
            if pp.polygon.fill_color == '#00ffff':
                rssi = -117
            if pp.polygon.fill_color == '#0000ff':
                rssi = -198
            if rssi == None:
                continue

            range_point = Rangearea.range_point(
                pp.latitude,
                pp.longitude,
                0, 
                rssi,
                'eui-313532352e005300')

            range_point_list.append(range_point)

        # Die erstellte range_point_list dem range_area Objekt hinzufügen
        range_area.add_range_point_list(range_point_list)

        # Analyse des Rangearea Objekts starten
        range_area.analyse() 

        # Nach der Analyse werden die ermittelten Polygone in der Datenbank gespeichert.
        # Dazu werden erstmal die Datenbanktabellen Polygon und Polygonpoints geleert.
        Polygonpoint.query.delete()
        Polygon.query.delete()
        db.session.commit()
        
        for polygon in range_area.polygon_list:

            new_polygon = Polygon(
                gtw_id=polygon['gtw_id'],
                fill_color=polygon['fill_color']
            )
            
            db.session.add(new_polygon)
            db.session.commit()

            for point in polygon['coords']:

                new_polygonpoint = Polygonpoint(
                    latitude=point[1],
                    longitude=point[0],
                    polygon_id=new_polygon.poly_id
                )
                
                db.session.add(new_polygonpoint)

            db.session.commit()

        # Log Eintrag hinzufügen
        current_dt = datetime.now()
        new_log = Log(modul='Polygon Builder', state='end', timestamp=current_dt.strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_log)
        db.session.commit()

        print('### Fertig ###')
        print('Alle Polygone gespeichert.')

    else:
        print('Zu wenige neue Punkte vorhanden: ', len(range_point_list))

