import numpy as np


def remove_special_tokens(l1, l2):
    l2 = l2[1:]
    l2 = l2[:len(l1)]
    return l1, l2


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


def get_model_index(in_array):
    if len(in_array.shape) == 3:
        in_array = np.argmax(in_array, axis=-1)
    return in_array


def ner(pred, label_encoder, tokenizer, problem, extract_ent=True):

    result_list = []
    pred[problem] = get_model_index(pred[problem])

    for input_ids, ner_pred in zip(pred['raw_text'].tolist(), pred[problem].tolist()):
        # tokens = tokenizer.convert_ids_to_tokens(input_ids)
        # tokens = [t.replace('[unused1]', ' ') for t in tokens]
        tokens = list(input_ids.decode('utf8'))
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
    pred[problem] = get_model_index(pred[problem])
    for input_ids, ner_pred in zip(pred['raw_text'].tolist(), pred[problem].tolist()):
        # tokens = tokenizer.convert_ids_to_tokens(input_ids)
        # tokens = [t.replace('[unused1]', ' ') for t in tokens]
        tokens = list(input_ids.decode('utf8'))
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


def seq_tag(pred, label_encoder, tokenizer, problem):
    result_list = []
    pred[problem] = get_model_index(pred[problem])
    for input_ids, ner_pred in zip(pred['raw_text'].tolist(), pred[problem].tolist()):
        # tokens = tokenizer.convert_ids_to_tokens(input_ids)
        # tokens = [t.replace('[unused1]', ' ') for t in tokens]
        tokens = list(input_ids.decode('utf8'))
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
        result_list.append(label[0])
    return result_list


def consolidate_ner(pred: dict, del_origin=True):
    new_pred = {'ner': []}
    for input_ind in range(len(pred['boson_ner'])):
        new_pred['ner'].append([])

        for ent, ent_type in pred['weibo_ner'][input_ind]:
            if ent_type in ['LOC', 'GPE']:
                new_pred['ner'][-1].append([ent, ent_type])
        for ent, ent_type in pred['boson_ner'][input_ind]:
            if ent_type != 'LOC':
                new_pred['ner'][-1].append([ent, ent_type])
    if del_origin:
        del pred['boson_ner'], pred['weibo_ner']
    pred.update(new_pred)
    return pred


def text_generation(pred, label_encoder, tokenizer, problem):
    result_list = []
    pred[problem] = get_model_index(pred[problem])
    for text_gen_pred in pred[problem].tolist():

        labels = label_encoder.convert_ids_to_tokens(text_gen_pred)
        result_list.append(''.join(labels).replace('##', ''))
    return result_list


def tag_generation(pred, label_encoder, tokenizer, problem):
    result_list = []
    pred[problem] = get_model_index(pred[problem])
    for text_gen_pred in pred[problem].tolist():

        labels = label_encoder.inverse_transform(text_gen_pred)
    return result_list


def parse_prediction(pred, label_encoder_dict, tokenizer, params):
    for problem in label_encoder_dict:
        if 'NER' == problem.split('_')[-1].upper():
            pred[problem] = np.array(ner(
                pred,
                label_encoder_dict[problem],
                tokenizer,
                problem,
                extract_ent=True))
        elif 'CWS' == problem.split('_')[-1].upper():
            pred[problem] = np.array(cws(
                pred,
                label_encoder_dict[problem],
                tokenizer,
                problem))
        elif params.problem_type[problem] == 'seq_tag':
            pred[problem] = np.array(seq_tag(
                pred,
                label_encoder_dict[problem],
                tokenizer,
                problem))
        elif params.problem_type[problem] == 'seq2seq_text':
            pred[problem] = np.array(text_generation(
                pred,
                label_encoder_dict[problem],
                tokenizer,
                problem
            ))
        elif params.problem_type[problem] == 'seq2seq_tag':
            pred[problem] = np.array(tag_generation(
                pred,
                label_encoder_dict[problem],
                tokenizer,
                problem
            ))
        else:
            try:
                pred[problem] = np.array(cls(
                    pred,
                    label_encoder_dict[problem],
                    tokenizer,
                    problem
                ))
            except:
                pass

    # pred = consolidate_ner(pred, del_origin=False)

    return pred
