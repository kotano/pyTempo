from tempo import tempoapp

# TODO: Can add argparse


def debug():
    tempoapp.TempoApp().run()


def main():
    app = tempoapp.TempoApp()
    try:
        app.run()
    except Exception as e:
        print(str(e))
        app.root.print_message(str(e), 30)

if __name__ == "__main__":
    # main()
    debug()
