import numpy as np


def remove_special_tokens(l1, l2):
    ind_list = []
    for ind, char in enumerate(l1):
        if char in ['[PAD]', '[CLS]', '[SEP]']:
            ind_list.append(ind)
    return [e for ie, e in enumerate(l1) if ie not in ind_list], [e for ie, e in enumerate(l2) if ie not in ind_list]


def merge_entity(tokens, labels):
    merged_tokens = []
    merged_labels = []
    for token, label in zip(tokens, labels):
        if label == 'O':
            merged_tokens.append(token)
            merged_labels.append(label)
        elif label[0] == 'B':
            merged_tokens.append(token)
            merged_labels.append(label[2:])
        elif label[0] in ['I', 'M', 'E']:
            try:
                merged_tokens[-1] += token
            except IndexError:
                merged_tokens.append(token)
                merged_labels.append(label)
        else:
            # strange label capture
            merged_tokens.append(token)
            merged_labels.append('O')
            # merged_labels[-1] += label
    return merged_tokens, merged_labels


def ner(pred, label_encoder, tokenizer, problem, extract_ent=True):

    result_list = []

    for input_ids, ner_pred in zip(pred['input_ids'].tolist(), pred[problem].tolist()):
        tokens = tokenizer.convert_ids_to_tokens(input_ids)
        tokens = [t.replace('[unused1]', ' ') for t in tokens]
        labels = label_encoder.inverse_transform(ner_pred)

        tokens, labels = remove_special_tokens(tokens, labels)

        tokens, labels = merge_entity(tokens, labels)
        if extract_ent:

            result_list.append([(ent, ent_type) for ent, ent_type in zip(
                tokens, labels) if ent_type != 'O'])

        else:
            result_list.append(
                list(zip(tokens, labels)))
    return result_list


def cws(pred, label_encoder, tokenizer, problem):
    result_list = []

    for input_ids, ner_pred in zip(pred['input_ids'].tolist(), pred[problem].tolist()):
        tokens = tokenizer.convert_ids_to_tokens(input_ids)
        tokens = [t.replace('[unused1]', ' ') for t in tokens]
        labels = label_encoder.inverse_transform(ner_pred)
        tokens, labels = remove_special_tokens(tokens, labels)
        output_str = ''
        for char, char_label in zip(tokens, labels):
            if char_label.lower() in ['s', 'e', 'o']:
                output_str += char + ' '
            else:
                output_str += char
        result_list.append(output_str)

    return result_list


def pos(pred, label_encoder, tokenizer, problem):
    result_list = []

    for input_ids, ner_pred in zip(pred['input_ids'].tolist(), pred[problem].tolist()):
        tokens = tokenizer.convert_ids_to_tokens(input_ids)
        tokens = [t.replace('[unused1]', ' ') for t in tokens]
        labels = label_encoder.inverse_transform(ner_pred)

        tokens, labels = remove_special_tokens(tokens, labels)
        tokens, labels = merge_entity(tokens, labels)

        result_list.append(
            list(zip(tokens, labels)))

    return result_list


def cls(pred, label_encoder, tokenizer, problem):
    result_list = []
    for pred in pred[problem].tolist():
        label = label_encoder.inverse_transform([np.argmax(pred)])
        result_list.append(label)
    return result_list


def parse_prediction(pred, label_encoder_dict, tokenizer):
    for problem in label_encoder_dict:
        if 'NER' in problem.upper():
            pred[problem] = np.array(ner(
                pred,
                label_encoder_dict[problem],
                tokenizer,
                problem))
        elif 'CWS' in problem.upper():
            pred[problem] = np.array(cws(
                pred,
                label_encoder_dict[problem],
                tokenizer,
                problem))
        elif 'POS' in problem.upper():
            pred[problem] = np.array(pos(
                pred,
                label_encoder_dict[problem],
                tokenizer,
                problem))
        elif 'emotion_analysis' in problem.lower():
            pred[problem] = np.array(cls(
                pred,
                label_encoder_dict[problem],
                tokenizer,
                problem
            ))

    return pred
