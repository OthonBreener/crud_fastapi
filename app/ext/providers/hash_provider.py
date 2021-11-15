from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])

def generation_hash(password):
    """
    Função que gera um hash apartir de uma string.
    Input:
        password: string
    Output:
        hash: string encriptografada
    """
    return pwd_context.hash(password)


def verification_hash(password, passord_hash):
    """
    Função que verifica se a string corresponde ao hash.
    Input:
        password: string
        passord_hash: string encriptografada
    Output:
        boolean: True ou False
    """

    return pwd_context.verify(password, passord_hash)
