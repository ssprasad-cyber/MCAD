import torch
import torchvision.transforms as T
from torchvision.models import resnet18
from PIL import Image


class AppearanceEncoder:

    def __init__(self, device="cpu"):

        self.device = device

        model = resnet18(pretrained=True)
        model.fc = torch.nn.Identity()

        self.model = model.to(device)
        self.model.eval()

        self.transform = T.Compose([
            T.Resize((256,128)),
            T.ToTensor(),
        ])


    def extract(self, frame):

        img = Image.fromarray(frame)

        tensor = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            emb = self.model(tensor)

        return emb.cpu().numpy().flatten()