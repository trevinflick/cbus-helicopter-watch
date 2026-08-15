def sendBluesky(photo, message, config):
    """Returns the created post's AT URI on success, or None if the message wasn't sent."""
    from atproto import Client
    from atproto_client.exceptions import AtProtocolError, UnauthorizedError
    sent = False
    post_uri = None
    retry_c = 0
    text = message if len(message) <= 300 else message[:297] + "..."
    while sent == False:
        try:
            client = Client()
            client.login(config.get('BLUESKY', 'HANDLE'), config.get('BLUESKY', 'APP_PASSWORD'))
            with open(photo, 'rb') as f:
                image_bytes = f.read()
            response = client.send_image(text=text, image=image_bytes, image_alt=message + "\nData: https://adsb.fi")
        except UnauthorizedError:
            print('Invalid Bluesky handle/app password, message not sent.')
            break
        except AtProtocolError as err:
            print('err.args:')
            print(err.args)
            print(f"Unexpected {err=}, {type(err)=}")
            if retry_c > 4:
                print('Bluesky attempts exceeded. Message not sent.')
                break
            retry_c += 1
            print('Bluesky retry count: ' + str(retry_c))
        except FileNotFoundError:
            print("Bluesky module couldn't find an image to send.")
            break
        else:
            sent = True
            post_uri = response.uri
            print("Bluesky message successfully sent.")
    return post_uri
