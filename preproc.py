

def encodage(df):

        code = {'tcp':0,'icmp':1,'udp':2,
            
            'ftp_data':0,'other':1,'private':2,'http':3,'remote_job':4,'name':5,'netbios_ns':6,'eco_i':7,'mtp':8,'telnet':9,
            'finger':10,'domain_u':11,'supdup':12,'uucp_path':13,'Z39_50':14,'smtp':15,'csnet_ns':16,'uucp':17,'netbios_dgm':18,
            'urp_i':19,'auth':20,'domain':21,'ftp':22,'bgp':23,'ldap':24, 'ecr_i':25,'gopher':26, 'vmnet':27,'systat':28,
            'http_443':29,'efs':30,'whois':31,'imap4':32,'iso_tsap':33,'echo':34,'klogin':35, 'link':36,'sunrpc':37,'login':38,
            'kshell':39,'sql_net':40,'time':41,'hostnames':42,'exec':43,'ntp_u':44,'discard':45,'nntp':46,'courier':47,'ctf':48,
            'ssh':49,'daytime':50,'shell':51,'netstat':52,'pop_3':53,'nnsp':54, 'IRC':55, 'pop_2':56,'printer':57,'tim_i':58 ,
            'pm_dump':59,'red_i':60,'netbios_ssn':61,'rje':62,'X11':63,'urh_i':64,'http_8001':65,'aol':66,'http_2784':67,'tftp_u':68,
            'harvest':69,
            'REJ':0,'SF':1,'RSTO':2,'S0':3,'RSTR':4,'SH':5,'S3':6,'S2':7,'S1':8,'RSTOS0':9,'OTH':10}
    
        
        for col in df.select_dtypes('object').columns:
            df.loc[:, col] = df[col].map(code)

        return df
# Usage example:
# preprocessor = Preprocessor()
# preprocessed_data = preprocessor.preprocess(data, labels)
