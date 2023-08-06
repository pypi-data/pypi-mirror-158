# EMO_AI
Use state-of-the-art to detect the user's emotion on social apps, particularly needed in modern society

## Installation
#### it's recommended to install pytorch via [official guide](https://pytorch.org/) first

    # stable version: have to install transformers, tokenizers, torch by hand ...
    pip install EMO-AI==0.0.2

    # latest version
    pip install EMO-AI


## Usage

    from EMO_AI.model_api import *
    from EMO_AI.data_process import *
    t = "Elvis is the king of rock"
    tokenizer = get_tokenizer()
    PATH = "your_pretrained_model.pt"
    # check how the model is saved in the first place
    model = get_model(PATH, inference_only=True)
    import torch
    with torch.no_grad():
            model.eval() # evaluate mode
            # convert_text_to_tensor(t) would work, but kinda slower and wasteful
            rep = model(convert_text_to_tensor(t, tokenizer))
    # print output tensor from forward pass
    print(rep)
    # get predicted emotion
    print_emotion(rep)

