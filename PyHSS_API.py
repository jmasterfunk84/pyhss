import sys
import json
from flask import Flask, request, jsonify, Response
from flask_restx import Api, Resource, fields, reqparse, abort
from werkzeug.middleware.proxy_fix import ProxyFix
app = Flask(__name__)


import logging
import yaml

with open("config.yaml", 'r') as stream:
    yaml_config = (yaml.safe_load(stream))

import os
import sys
sys.path.append(os.path.realpath('lib'))

#Setup Logging
import logtool

import database
APN = database.APN
Serving_APN = database.SERVING_APN
AUC = database.AUC
SUBSCRIBER = database.SUBSCRIBER
IMS_SUBSCRIBER = database.IMS_SUBSCRIBER
TFT = database.TFT
CHARGING_RULE = database.CHARGING_RULE


app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='PyHSS OAM API',
    description='Restful API for working with PyHSS',
    doc='/docs/'
)

ns_apn = api.namespace('apn', description='PyHSS APN Functions')
ns_auc = api.namespace('auc', description='PyHSS AUC Functions')
ns_subscriber = api.namespace('subscriber', description='PyHSS SUBSCRIBER Functions')
ns_ims_subscriber = api.namespace('ims_subscriber', description='PyHSS IMS SUBSCRIBER Functions')
ns_tft = api.namespace('tft', description='PyHSS TFT Functions')
ns_charging_rule = api.namespace('charging_rule', description='PyHSS Charging Rule Functions')

ns_oam = api.namespace('oam', description='PyHSS OAM Functions')
ns_pcrf = api.namespace('PCRF', description='PyHSS PCRF Dynamic Functions')

parser = reqparse.RequestParser()
parser.add_argument('APN JSON', type=str, help='APN Body')

APN_model = api.schema_model('APN JSON', 
    database.Generate_JSON_Model_for_Flask(APN)
)
Serving_APN_model = api.schema_model('Serving APN JSON', 
    database.Generate_JSON_Model_for_Flask(Serving_APN)
)
AUC_model = api.schema_model('AUC JSON', 
    database.Generate_JSON_Model_for_Flask(AUC)
)
SUBSCRIBER_model = api.schema_model('SUBSCRIBER JSON', 
    database.Generate_JSON_Model_for_Flask(SUBSCRIBER)
)
IMS_SUBSCRIBER_model = api.schema_model('IMS_SUBSCRIBER JSON', 
    database.Generate_JSON_Model_for_Flask(IMS_SUBSCRIBER)
)
TFT_model = api.schema_model('TFT JSON', 
    database.Generate_JSON_Model_for_Flask(TFT)
)
CHARGING_RULE_model = api.schema_model('CHARGING_RULE JSON', 
    database.Generate_JSON_Model_for_Flask(CHARGING_RULE)
)

PCRF_Push_model = api.model('PCRF_Rule', {
    'imsi': fields.String(required=True, description='IMSI of Subscriber to push rule to'),
    'apn_id': fields.Integer(required=True, description='APN_ID of APN to push rule on'),
    'charging_rule_id' : fields.Integer(required=True, description='charging_rule_id to push'),
})

@ns_apn.route('/<string:apn_id>')
class PyHSS_APN_Get(Resource):
    def get(self, apn_id):
        '''Get all APN data for specified APN ID'''
        try:
            apn_data = database.GetObj(APN, apn_id)
            return apn_data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    def delete(self, apn_id):
        '''Delete all APN data for specified APN ID'''
        try:
            apn_data = database.DeleteObj(APN, apn_id)
            return apn_data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    @ns_apn.doc('Update APN Object')
    @ns_apn.expect(APN_model)
    def patch(self, apn_id):
        '''Update APN data for specified APN ID'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            apn_data = database.UpdateObj(APN, json_data, apn_id)
            print("Updated object")
            print(apn_data)
            return apn_data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500   

@ns_apn.route('/')
class PyHSS_APN(Resource):
    @ns_apn.doc('Create APN Object')
    @ns_apn.expect(APN_model)
    def put(self):
        '''Create new APN'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            apn_id = database.CreateObj(APN, json_data)
            return apn_id, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_auc.route('/<string:auc_id>')
class PyHSS_AUC_Get(Resource):
    def get(self, auc_id):
        '''Get all AuC data for specified AuC ID'''
        try:
            apn_data = database.GetObj(AUC, auc_id)
            return apn_data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    def delete(self, auc_id):
        '''Delete all AUC data for specified AUC ID'''
        try:
            data = database.DeleteObj(AUC, auc_id)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    @ns_auc.doc('Update AUC Object')
    @ns_auc.expect(AUC_model)
    def patch(self, auc_id):
        '''Update AuC data for specified AuC ID'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            data = database.UpdateObj(AUC, json_data, auc_id)
            print("Updated object")
            print(data)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_auc.route('/')
class PyHSS_AUC(Resource):
    @ns_auc.doc('Create AUC Object')
    @ns_auc.expect(AUC_model)
    def put(self):
        '''Create new AUC'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            data = database.CreateObj(AUC, json_data)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_subscriber.route('/<string:subscriber_id>')
class PyHSS_SUBSCRIBER_Get(Resource):
    def get(self, subscriber_id):
        '''Get all SUBSCRIBER data for specified subscriber_id'''
        try:
            apn_data = database.GetObj(SUBSCRIBER, subscriber_id)
            return apn_data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    def delete(self, subscriber_id):
        '''Delete all data for specified subscriber_id'''
        try:
            data = database.DeleteObj(SUBSCRIBER, subscriber_id)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    @ns_subscriber.doc('Update SUBSCRIBER Object')
    @ns_subscriber.expect(SUBSCRIBER_model)
    def patch(self, subscriber_id):
        '''Update SUBSCRIBER data for specified subscriber_id'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            data = database.UpdateObj(SUBSCRIBER, json_data, subscriber_id)
            print("Updated object")
            print(data)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_subscriber.route('/')
class PyHSS_SUBSCRIBER(Resource):
    @ns_subscriber.doc('Create SUBSCRIBER Object')
    @ns_subscriber.expect(SUBSCRIBER_model)
    def put(self):
        '''Create new SUBSCRIBER'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            data = database.CreateObj(SUBSCRIBER, json_data)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_ims_subscriber.route('/<string:ims_subscriber_id>')
class PyHSS_IMS_SUBSCRIBER_Get(Resource):
    def get(self, ims_subscriber_id):
        '''Get all SUBSCRIBER data for specified ims_subscriber_id'''
        try:
            apn_data = database.GetObj(IMS_SUBSCRIBER, ims_subscriber_id)
            return apn_data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    def delete(self, ims_subscriber_id):
        '''Delete all data for specified ims_subscriber_id'''
        try:
            data = database.DeleteObj(IMS_SUBSCRIBER, ims_subscriber_id)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    @ns_ims_subscriber.doc('Update IMS SUBSCRIBER Object')
    @ns_ims_subscriber.expect(IMS_SUBSCRIBER_model)
    def patch(self, ims_subscriber_id):
        '''Update IMS SUBSCRIBER data for specified ims_subscriber'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            data = database.UpdateObj(IMS_SUBSCRIBER, json_data, ims_subscriber_id)
            print("Updated object")
            print(data)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_ims_subscriber.route('/')
class PyHSS_IMS_SUBSCRIBER(Resource):
    @ns_ims_subscriber.doc('Create IMS SUBSCRIBER Object')
    @ns_ims_subscriber.expect(IMS_SUBSCRIBER_model)
    def put(self):
        '''Create new IMS SUBSCRIBER'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            data = database.CreateObj(IMS_SUBSCRIBER, json_data)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_tft.route('/<string:tft_id>')
class PyHSS_TFT_Get(Resource):
    def get(self, tft_id):
        '''Get all TFT data for specified tft_id'''
        try:
            apn_data = database.GetObj(TFT, tft_id)
            return apn_data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    def delete(self, tft_id):
        '''Delete all data for specified tft_id'''
        try:
            data = database.DeleteObj(TFT, tft_id)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    @ns_ims_subscriber.doc('Update IMS tft_id Object')
    @ns_ims_subscriber.expect(TFT_model)
    def patch(self, tft_id):
        '''Update tft_id data for specified tft_id'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            data = database.UpdateObj(TFT, json_data, tft_id)
            print("Updated object")
            print(data)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_tft.route('/')
class PyHSS_TFT(Resource):
    @ns_ims_subscriber.doc('Create TFT Object')
    @ns_ims_subscriber.expect(TFT_model)
    def put(self):
        '''Create new TFT'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            data = database.CreateObj(TFT, json_data)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_charging_rule.route('/<string:charging_rule_id>')
class PyHSS_Charging_Rule_Get(Resource):
    def get(self, charging_rule_id):
        '''Get all Charging Rule data for specified charging_rule_id'''
        try:
            apn_data = database.GetObj(CHARGING_RULE, charging_rule_id)
            return apn_data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    def delete(self, charging_rule_id):
        '''Delete all data for specified charging_rule_id'''
        try:
            data = database.DeleteObj(CHARGING_RULE, charging_rule_id)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

    @ns_charging_rule.doc('Update charging_rule_id Object')
    @ns_charging_rule.expect(CHARGING_RULE_model)
    def patch(self, charging_rule_id):
        '''Update charging_rule_id data for specified charging_rule_id'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            data = database.UpdateObj(CHARGING_RULE, json_data, charging_rule_id)
            print("Updated object")
            print(data)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_charging_rule.route('/')
class PyHSS_Charging_Rule(Resource):
    @ns_charging_rule.doc('Create ChargingRule Object')
    @ns_charging_rule.expect(CHARGING_RULE_model)
    def put(self):
        '''Create new ChargingRule'''
        try:
            json_data = request.get_json(force=True)
            print("JSON Data sent: " + str(json_data))
            data = database.CreateObj(CHARGING_RULE, json_data)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500


@ns_oam.route('/diameter_peers')
class PyHSS_OAM_Peers(Resource):
    def get(self):
        '''Get all Diameter Peers'''
        try:
            logObj = logtool.LogTool()
            DiameterPeers = logObj.GetDiameterPeers()
            return DiameterPeers, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_oam.route('/serving_subs')
class PyHSS_OAM_Serving_Subs(Resource):
    def get(self):
        '''Get all Subscribers served by HSS'''
        try:
            data = database.Get_Served_Subscribers()
            print("Got back served Subs: " + str(data))
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_oam.route('/serving_subs_pcrf')
class PyHSS_OAM_Serving_Subs_PCRF(Resource):
    def get(self):
        '''Get all Subscribers served by PCRF'''
        try:
            data = database.Get_Served_PCRF_Subscribers()
            print("Got back served Subs: " + str(data))
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_oam.route('/serving_subs_ims')
class PyHSS_OAM_Serving_Subs_IMS(Resource):
    def get(self):
        '''Get all Subscribers served by IMS'''
        try:
            data = database.Get_Served_IMS_Subscribers()
            print("Got back served Subs: " + str(data))
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_oam.route('/subscriber/<string:imsi>')
class PyHSS_OAM_Subscriber(Resource):
    def get(self, imsi):
        '''Get data for IMSI'''
        try:
            data = database.Get_Subscriber(imsi=imsi)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_oam.route('/subscriber_msisdn/<string:msisdn>')
class PyHSS_OAM_Subscriber(Resource):
    def get(self, msisdn):
        '''Get data for MSISDN'''
        try:
            data = database.Get_Subscriber(msisdn=msisdn)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500

@ns_pcrf.route('/')
class PyHSS_PCRF(Resource):
    @ns_pcrf.doc('Push Charging Rule to a Subscriber')
    @ns_pcrf.expect(PCRF_Push_model)
    def put(self):
        '''Push predefined Charging Rule to Subscriber'''
    
        json_data = request.get_json(force=True)
        print("JSON Data sent: " + str(json_data))
        #Get IMSI
        subscriber_data = database.Get_Subscriber(imsi=str(json_data['imsi']))
        print("subscriber_data: " + str(subscriber_data))

        #Get PCRF Session
        pcrf_session_data = database.Get_Serving_APN_Subscriber(subscriber_id=subscriber_data['subscriber_id'], apn_id=json_data['apn_id'])          
        print("pcrf_session_data: " + str(pcrf_session_data))

        #Get Charging Rules
        ChargingRule = database.Get_Charging_Rule(json_data['charging_rule_id'])
        ChargingRule['apn_data'] = database.Get_APN(json_data['apn_id'])
        print("Got ChargingRule: " + str(ChargingRule))

        diameter_host = yaml_config['hss']['OriginHost']                                                        #Diameter Host of this Machine
        OriginRealm = yaml_config['hss']['OriginRealm']
        DestinationRealm = OriginRealm
        mcc = yaml_config['hss']['MCC']                                                                     #Mobile Country Code
        mnc = yaml_config['hss']['MNC']                                                                      #Mobile Network Code
        import diameter
        diameter = diameter.Diameter(diameter_host, DestinationRealm, 'PyHSS-client-API', str(mcc), str(mnc))
        diam_hex = diameter.Request_16777238_258(pcrf_session_data['pcrf_session_id'], ChargingRule, pcrf_session_data['ue_ip'], pcrf_session_data['serving_pgw'], 'ServingRealm.com')
        import time
        logObj = logtool.LogTool()
        logObj.Async_SendRequest(diam_hex, str(pcrf_session_data['serving_pgw']))
        return diam_hex, 200

@ns_pcrf.route('/<string:charging_rule_id>')
class PyHSS_OAM_Subscriber(Resource):
    def get(self, charging_rule_id):
        '''Get full Charging Rule + TFTs'''
        try:
            data = database.Get_Charging_Rule(charging_rule_id)
            return data, 200
        except Exception as E:
            print(E)
            response_json = {'result': 'Failed', 'Reason' : str(E)}
            return jsonify(response_json), 500


if __name__ == '__main__':
    app.run(debug=True)
