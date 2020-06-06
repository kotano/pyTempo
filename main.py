from tempo import tempoapp

# TODO: Can add argparse


def main():
    tempoapp.TempoApp().run()


def debug():
    app = tempoapp.TempoApp()
    try:
        app.run()
    except Exception as e:
        app.root.print_message(e, 15)
        print(e)

if __name__ == "__main__":
    debug()
