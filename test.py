from src import pyhog_engine_xXLarryTFVWXx as pyhog
pyhog.on()

def main():
    while True:
        try:
            pyhog.process([])
        except SystemExit:
            pyhog.files.save_game("Test", "Null", "Lorem Ipsum".encode("ECMA-94"))
            pyhog.off()
            return


if __name__ == "__main__":
    main()
pyhog.off()