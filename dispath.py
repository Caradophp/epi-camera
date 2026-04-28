from datetime import datetime
from db.mysql_connection import Mysql  # Certifique-se de que o nome do arquivo esteja correto
from log import Log
import cv2

class Dispath:
    
    # Inicialização dos classificadores (mantidos como variáveis de classe conforme original)
    modelo_luvas = cv2.CascadeClassifier('model/haarcascade_hand.xml')
    modelo_capacete = cv2.CascadeClassifier('model/capacete.xml')
    modelo_oculos = cv2.CascadeClassifier('model/haarcascade_eye_tree_eyeglasses.xml')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
    aux = False
    logger = Log("data.log")
    
    def __init__(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            self.verify_helmet(frame)
            self.verify_gloves(frame)
            self.verify_glasses(frame)

            cv2.imshow("teste", frame)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        
    def _salvar_evento(self, mensagem):
        """Método auxiliar para centralizar a gravação no MySQL"""
        sql = "INSERT INTO eventos (evento, data) VALUES (%s, %s)"
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            Mysql.execute(sql, (mensagem, data_atual))
        except Exception as e:
            self.logger.write(f"Erro ao salvar no MySQL: {str(e)}")

    def verify_helmet(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        capacetes = self.modelo_capacete.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in capacetes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Capacete', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        if len(capacetes) == 0:
            if not self.aux:
                self._salvar_evento("Sem capacete detectado!")
                self.aux = True
            
            # Detecção de face para marcar onde deveria estar o capacete
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, 'Sem capacete', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                
    def verify_gloves(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            maos = self.modelo_luvas.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            maos_validas = []

            for (mx, my, mw, mh) in maos:
                esta_no_rosto = False
                centro_x, centro_y = mx + mw//2, my + mh//2
                
                for (fx, fy, fw, fh) in faces:
                    if (fx < centro_x < fx + fw) and (fy < centro_y < fy + fh):
                        esta_no_rosto = True
                        break
                
                if not esta_no_rosto:
                    maos_validas.append((mx, my, mw, mh))
                    cv2.rectangle(frame, (mx, my), (mx+mw, my+mh), (255, 165, 0), 2)
                    cv2.putText(frame, "Luva Detectada", (mx, my-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0), 2)

            if len(maos_validas) == 0:
                self._salvar_evento("Sem luvas detectado!")
                
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, 'Sem luvas', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                
        except Exception as e:
            self.logger.write("Erro ao detectar luvas: " + str(e))
            
    def verify_glasses(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            oculos = self.modelo_oculos.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            
            for (x, y, w, h) in oculos:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(frame, 'Oculos', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                
            if len(oculos) == 0:
                self._salvar_evento("Sem oculos detectado!")
                
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    cv2.putText(frame, 'Sem oculos', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        except Exception as e:
            self.logger.write("Erro ao detectar oculos: " + str(e))