import db_irsol.pre_build_functions as db_irsol_functions
from db_irsol.entities.default_entity import DefaultEntity
from db_irsol.entities.observation import Observation
from db_irsol.entities.measurement import Measurement

manager = db_irsol_functions.get_manager_gateways_from_validation_params('db_irsol_client_admin', 'qnpZc^wa2"\DqPy~')

observation, measurements = db_irsol_functions.get_observation_and_measurements_from_dir(
        "/home/mushu/Desktop/irsol/data/irsol_new/2021/210526", manager)

for measurement in measurements:
        print(measurement.get_parameters())

#db_irsol_functions.insert_observation_and_measurements_on_server(observation, measurements)


'''
gg = manager.get_default_gateway("Measurement.php").get_by_parameters({"fk_observation": 1})

counter = 0
for g in gg:
        for f in measurements:
                f_p = f.get_parameters()
                if g['name'] == f_p['name'] and int(g['pigi']) == int(f_p['pigi']):
                        counter += 1
                elif g['name'] == f_p['name']:
                        print(g['name'])
                        print(int(f_p['pigi']))
                        print(int(g['pigi']))

print(counter)'''


