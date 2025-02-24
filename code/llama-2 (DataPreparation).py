# -*- coding: utf-8 -*-
"""Llama-2 (Tag generation).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VM2X2Z-ft0xw8M2-NUGVbwy6wH-cFza6
"""

class TGDataset(torch.utils.data.Dataset):
    def __init__(self, data, tokenizer, max_len, is_eval):
        self.data = data
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.is_eval = is_eval

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
      row_data = self.data.iloc[index]
      prompt = generate_prompt(row_data, self.is_eval)
      prompt_encoding = self.tokenizer(
          prompt,
          max_length = self.max_len,
          padding = 'max_length',
          truncation = True,
          add_special_tokens = True,
          return_tensors = 'pt',
      )
      input_ids = prompt_encoding['input_ids'].squeeze()
      attention_mask = prompt_encoding['attention_mask'].squeeze()

      if self.is_eval == False:
        response_index = get_response_index(input_ids, 'TG')
        if response_index:
          labels = torch.cat((torch.full((response_index,), -100), input_ids[response_index:])).squeeze()
        else:
          print('response_index not found')
      else:
        labels = self.tokenizer(
            row_data['tags'] + '</s>',
            add_special_tokens = False,
            return_tensors='pt',
        )
        labels = labels['input_ids'].squeeze()
      return {
          'input_ids': input_ids,
          'attention_mask': attention_mask,
          'labels': labels
      }

class TGDataModule(pl.LightningDataModule):
    def __init__(self, data, tokenizer, script_args):
        super().__init__()
        self.data = data
        self.tokenizer = tokenizer
        self.per_device_train_batch_size = script_args.per_device_train_batch_size
        self.per_device_eval_batch_size = script_args.per_device_eval_batch_size
        self.max_len = script_args.max_seq_length
        self.setup()

    def setup(self, stage=None):
        len_tr = int(script_args.split_ratio[0] * self.data.shape[0])
        len_te = int(script_args.split_ratio[1] * self.data.shape[0])
        train_data, test_data = train_test_split(self.data,
                                                 test_size=len_te,
                                                 random_state=42)
        train_data.reset_index(drop=True, inplace=True)
        test_data.reset_index(drop=True, inplace=True)

        self.train_data = TGDataset(train_data, self.tokenizer, self.max_len, is_eval=False)
        self.test_data = TGDataset(test_data, self.tokenizer, self.max_len, is_eval=True)

    def train_dataloader(self):
        return torch.utils.data.DataLoader(
            self.train_data,
            batch_size=self.per_device_train_batch_size,
            shuffle=True,
            num_workers=8,
        )

    def test_dataloader(self):
        return torch.utils.data.DataLoader(
            self.test_data,
            sampler = torch.utils.data.SequentialSampler(self.test_data,),
            batch_size= self.per_device_eval_batch_size,
            num_workers=8
        )