
class PredictionPipeline:
    def __init__(self):
        os.system("dvc repro")
        model_path = os.path.join("artifacts","training", "model.h5")
        self.model = load_model(model_path)
    def get_embeddings_codebert(code_corpus):
        embeddings = []
        for code in code_corpus:
            tokens_ids = embedding_model.tokenize([code],mode="<encoder-only>")
            source_ids = torch.tensor(tokens_ids).to(device)
            tokens_embeddings,nl_embedding = embedding_model(source_ids)
            norm_nl_embedding = torch.nn.functional.normalize(nl_embedding, p=2, dim=1)
            norm_nl_embedding = norm_nl_embedding.detach().cpu().numpy()[0].tolist()
            embeddings.append(norm_nl_embedding)
        return embeddings
    def predict(self, fileimg):
            # load model

            image = cv2.imread(fileimg)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_image = cv2.resize(gray_image, [100, 120])
            gray_image = gray_image.reshape(1, 100, 120, 1)
            predicted_class = np.argmax(self.model.predict(gray_image))

            if predicted_class == 0:
                prediction = "Blank"
            elif predicted_class == 1:
                prediction =  "Ok"
            elif predicted_class == 2:
                prediction =  "Thumbs Up"
            elif predicted_class == 3:
                prediction =  "Thumbs Down"
            elif predicted_class == 4:
                prediction =  "Punch"
            elif predicted_class == 5:
                prediction = "High Five"
            return prediction