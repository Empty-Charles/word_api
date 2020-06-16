#用于数据库连接操作
import pymysql
class Db_Manager:
    def __init__(self,receive):
        self.__host ="rm-bp1wkh230i726zd7amo.mysql.rds.aliyuncs.com"# host地址
        self.__port = 3306  # 端口号
        self.__user = "pydev"  # 用户名
        self.__password = "vFfMlvDIKyAlzvFNwjnr"  # 密码
        self.__db = "pyword_api_test"  # 数据库名
        self.receive = receive
        self.level = receive.option.level
        self.word = receive.word
    # 连接数据库
    # 返回连接
    def __connect(self):
        conn = pymysql.Connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
            db=self.__db,
        )
        self.cursor = conn.cursor()  # 创建游标

    #
    # 得到用户信息
    # 传入用户名
    # 返回密钥 0：不存在该用户

    def get_user_data(self):
        self.__connect()
        name = self.receive.security.uname
        sql = "SELECT * FROM t_user WHERE u_name=%s"

        # sql = 'select * from t_user WHERE u_name = name '
        self.cursor.execute(sql)
        result = self.cursor.fetchall()  # 接受全部返回内容
        if result==():
            return 0
        for row in result:
            username = row[0]
            key = row[1]
        self.close()
        return key


    # 返回游标
    # 断开连接
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 得到要发送的数据
    # 返回Send类
    # 返回值：1：没用该单词
    #        0：正常查询
    #        2：服务器错误
    def get_send_data(self):
        self.__connect()
        word =self.word
        print(word)
        sql = "SELECT * FROM t_word WHERE word=%s"
        self.cursor.execute(sql,word)
        result = self.cursor.fetchall()  # 接受全部返回内容
        if result ==():
            return "NULL"
        for row in result:
            wordT = row[0]
            word_translation = row[1]
            sentences = row[2]
        if wordT is None:
            self.close()
            return 1

        sentences_bak=self.get_sentences(sentences=sentences)
        length =sentences_bak[1]
        sentences_list =sentences_bak[0]

        '''接收的结果为一个三维数组'''
        return (self.word,word_translation,sentences_list,length)


    def get_sentences(self,sentences):
        sentences_id = sentences.split("|")  # 切割句子id
        sentences_list = [[0] * 4 for i in range(len(sentences_id))]  # 创建列表存每个句子
        # sss={}
        # print(sentences)
        z = 0
        for i in range(len(sentences_id)):
            sql = "SELECT * FROM t_sentence WHERE s_id=%s"
            self.cursor.execute(sql, sentences_id[i])
            result = self.cursor.fetchall()  # 接受全部返回内容

            for row in result:
                s_en = row[1]
                s_cn = row[2]
                s_voice = row[3]
                s_level = row[4]
                f_name = row[5]
            # print(s_level)
            if s_level == self.level:
                sentences_list[z][0] = f_name
                sentences_list[z][1] = s_cn
                sentences_list[z][2] = s_en
                sentences_list[z][3] = s_voice
                z = z + 1

                ''' "fname":"电影名",
                            "en":"英文原版例句",
                            "cn":"中文翻译例句",
                            "voice":"音频文件地址"'''
                '''想以字典形式返回

                j = {z: {
                    "en":s_en,
                    "cn":s_cn,
                    "voice":s_voice,
                    "film":f_name
                }}
                sss.update(j)'''

        length = z
        return(sentences_list,length)