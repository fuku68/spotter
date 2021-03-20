from src.slackbot import sender
from src.aws import ec2

def main() -> None:
    sender.send_instance_list()
    # sender.send_select_instance()
    # ec2.cancel_spot_instance('sir-ie7gbnxn')
    # ec2.create_spot_instance('t1.micro')
    ec2.terminate_instance('i-0f25f1ac8feee1c39')


if __name__ == "__main__":
    main()
