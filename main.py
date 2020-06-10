from tempo import tempoapp

# TODO: Can add argparse


def main():
    tempoapp.TempoApp().run()


def debug():
    app = tempoapp.TempoApp()
    try:
        app.run()
    except Exception as e:
        print(e)
        app.root.print_message(e, 15)

if __name__ == "__main__":
    debug()
    # main()
