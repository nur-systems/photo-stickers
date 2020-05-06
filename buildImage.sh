# Get the BASNet repo
git clone https://github.com/NathanUA/BASNet

# Download the pretrained model
mkdir -p BASNet/saved_models/basnet_bsi
fileid="1s52ek_4YTDRt_EOkx1FS53u-vJa0c4nu"
wget --save-cookies cookies.txt 'https://docs.google.com/uc?export=download&id='$fileid -O- \
     | grep -o '/uc[^"]*' | grep confirm | sed 's/amp;//g' > confirm.txt
wget --load-cookies cookies.txt -O BASNet/saved_models/basnet_bsi/basnet.pth \
     "https://docs.google.com$(<confirm.txt)"
rm confirm.txt cookies.txt

# Fetch the resnet 34 pretrained model
curl https://download.pytorch.org/models/resnet34-333f7ec4.pth -o resnet34-333f7ec4.pth

# Build the docker image
docker build -t basnet .
docker run --rm -p 8080:8080 basnet
