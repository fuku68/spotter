from src.slackbot import send
from src.aws import ec2

def main() -> None:
    # send.send_instance_list()
    # send.send_select_instance()
    ec2.cancel_spot_instance('sir-ie7gbnxn')
    # ec2.create_spot_instance('t1.micro')


if __name__ == "__main__":
    main()
