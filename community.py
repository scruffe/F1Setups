import tkinter
import tkinter.ttk
import grid_widgets


class CommunityWidget:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Community')

        self.cmd = Commands()

        self.upload_button = None
        self.download_button = None
        self.search_button = None

        self.create_buttons()
        self.buttons = [self.search_button, self.upload_button, self.download_button]

        self.track = None
        self.uploaded_by = None
        self.downloads = None
        self.date_uploaded = None

        self.create_labels()
        self.labels = [self.track, self.uploaded_by, self.downloads, self.date_uploaded]

        self.grid()

    def create_buttons(self):
        self.search_button = tkinter.Button(
            self.window,
            text="Search",
            command=self.cmd.search())
        self.upload_button = tkinter.Button(
            self.window,
            text="Upload",
            command=self.cmd.upload())
        self.download_button = tkinter.Button(
            self.window,
            text="Download",
            command=self.cmd.download())

    def create_labels(self):
        self.track = tkinter.Label(
            self.window,
            text="Track",
            anchor=tkinter.W
        )
        self.uploaded_by = tkinter.Label(
            self.window,
            text="Uploaded by:",
            anchor=tkinter.W
        )
        self.downloads = tkinter.Label(
            self.window,
            text="downloads",
            anchor=tkinter.W
        )
        self.date_uploaded = tkinter.Label(
            self.window,
            text="Uploaded",
            anchor=tkinter.W
        )

    def grid(self):
        box1 = grid_widgets.GridWidgets(increment_horizontal=True)
        for label in self.labels:
            box1.grid_box(label)

        box2 = grid_widgets.GridWidgets(startrow=(box1.row + 1),increment_horizontal=True)
        for button in self.buttons:
            box2.grid_box(button, rowspan=3)




class Commands:
    def __init__(self):
        pass

    def sort(self):
        """ sort on downloads"""
        pass

    def upload(self):
        """
        user name
        upload setup to online db
        """
        pass

    def download(self):
        # download file
        # downloads++
        pass

    def search(self):
        pass



if __name__ == "__main__":
    CommunityWidget()


