import { ReactNotificationOptions, store } from "react-notifications-component";

class NotificationProvider {
    static createNotification = (title: string, message: string, type: ReactNotificationOptions["type"]
    , timemsec: number = 5000): void => {
        store.addNotification({
            title: title,
            message: message,
            type: type,
            insert: "top",
            container: "top-right",
            animationIn: ["animate__animated", "animate__fadeIn"],
            animationOut: ["animate__animated", "animate__fadeOut"],
            dismiss: {
              duration: timemsec,
              onScreen: true
            }
          })
    }
    
  static createError = (message: string, timems: number = 10000) => {
    console.log(message);
    NotificationProvider.createNotification("Ошибка", message, "danger", timems);
  }
}

export default NotificationProvider;