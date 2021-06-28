import helper

def create_file_rsa(filename,rsa_priv,rsa_pub):
    private_key_start_comment = '-----BEGIN RSA PRIVATE KEY-----\n'
    private_key_end_comment = '-----END RSA PRIVATE KEY-----'
    public_key_start_comment = '-----BEGIN PUBLIC KEY-----\n'
    public_key_end_comment = '-----END PUBLIC KEY-----'
    print(rsa_priv,rsa_pub)
    base64_rsa_priv=helper.convert_to_base64(rsa_priv)
    base64_rsa_pub=helper.convert_to_base64(rsa_pub)
    
    #fprivClear= open(str(filename)+".priv","w")
    #fpubClear = open(str(filename)+".pub","w")
    fpriv= open(str(filename)+".priv","w+")
    fpub = open(str(filename)+".pub","w+")
    for i in range(3):
        if(i == 0):
            fpriv.write(private_key_start_comment)
            fpub.write(public_key_start_comment)
        if(i == 1):
            fpriv.write(base64_rsa_priv+"\n")
            fpub.write(base64_rsa_pub+"\n")
        if(i == 2):
            fpriv.write(private_key_end_comment)
            fpub.write(public_key_end_comment)
    fpriv.close()
    fpub.close() 
    return "File created"
