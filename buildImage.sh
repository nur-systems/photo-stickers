# Get the BASNet repo
git clone https://github.com/NathanUA/BASNet

# Move it into the source directory
mv BASNet/ src/pystickers/

# Download the pretrained model
mkdir -p src/pystickers/BASNet/saved_models/basnet_bsi
fileid="1s52ek_4YTDRt_EOkx1FS53u-vJa0c4nu"
wget --save-cookies cookies.txt 'https://docs.google.com/uc?export=download&id='$fileid -O- \
     | grep -o '/uc[^"]*' | grep confirm | sed 's/amp;//g' > confirm.txt
wget --load-cookies cookies.txt -O src/pystickers/BASNet/saved_models/basnet_bsi/basnet.pth \
     "https://docs.google.com$(<confirm.txt)"
rm -f confirm.txt cookies.txt

# Fetch the resnet 34 pretrained model
curl https://download.pytorch.org/models/resnet34-333f7ec4.pth -o resnet34-333f7ec4.pth

# Clean the BASNet repo if needed
rm -rf BASNet

# Run tests
pip install -r requirements.txt
python3 -m pytest --rootdir=tests/ --ignore src/pystickers/BASNet || exit 1

# Build the docker image
docker build -t sticker-basnet .

# Push to DockerHub
COMMIT_HASH=$(git rev-parse --short HEAD)
docker tag sticker-basnet:latest nursystems/sticker-basnet:$COMMIT_HASH
docker push nursystems/sticker-basnet:$COMMIT_HASH

# Run the docker image with all available GPUs
if command -v nvidia-smi ; then
  GPU_COMMAND="--gpus all"
fi
docker run --rm $GPU_COMMAND -d -p 8000:80 nursystems/sticker-basnet:$COMMIT_HASH
