'''import db_irsol.api_gateway.authenticate_gateway as auth
import db_irsol.api_gateway.default_gateway as gate

entity = auth.AuthenticateGateway('db_irsol_client', 'qnpZc^wa2"\DqPy~')
tele = gate.DefaultGateway("User", entity)

print(tele.get_chunk(0, 5))'''

import db_irsol.entities.utility as util

print(util.unzip_file("fff"))