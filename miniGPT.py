import torch
import torch.nn as nn
import torch.nn.functional as F

class SelfAttentionHead(nn.Module):
    def __init__(self, emb_dim, head_size, block_size):
        super().__init__()
        self.key = nn.Linear(emb_dim, head_size, bias=False)
        self.query = nn.Linear(emb_dim, head_size, bias=False)
        self.value = nn.Linear(emb_dim, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))
        self.dropout = nn.Dropout(0.1)  # optional, for regularization
        self.head_size = head_size

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)     # (B, T, head_size)
        q = self.query(x)   # (B, T, head_size)

        attn = (q @ k.transpose(-2, -1)) / (self.head_size ** 0.5)  # (B, T, T)
        attn = attn.masked_fill(self.tril[:T, :T] == 0, float('-inf'))  # masking
        attn = F.softmax(attn, dim=-1)  # attention scores
        attn = self.dropout(attn)

        v = self.value(x)   # (B, T, head_size)
        out = attn @ v      # (B, T, head_size)
        return out

class MultiHeadAttention(nn.Module):
    def __init__(self, emb_dim, num_heads, block_size):
        super().__init__()
        self.heads = nn.ModuleList([SelfAttentionHead(emb_dim, emb_dim // num_heads, block_size) for _ in range(num_heads)])
        self.proj = nn.Linear(emb_dim, emb_dim)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.proj(out)
        out = self.dropout(out)
        return out

class FeedForward(nn.Module):
    def __init__(self, emb_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(emb_dim, 4 * emb_dim),
            nn.ReLU(),
            nn.Linear(4 * emb_dim, emb_dim),
            nn.Dropout(0.1),
        )

    def forward(self, x):
        return self.net(x)

class TransformerBlock(nn.Module):
    def __init__(self, emb_dim, num_heads, block_size):
        super().__init__()
        self.ln1 = nn.LayerNorm(emb_dim)
        self.ln2 = nn.LayerNorm(emb_dim)
        self.attn = MultiHeadAttention(emb_dim, num_heads, block_size)
        self.ff = FeedForward(emb_dim)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ff(self.ln2(x))
        return x

class MiniGPT(nn.Module):
    def __init__(self, vocab_size, block_size, emb_dim, n_layers, n_heads):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, emb_dim)
        self.position_embedding = nn.Embedding(block_size, emb_dim)
        self.blocks = nn.Sequential(*[TransformerBlock(emb_dim, n_heads, block_size) for _ in range(n_layers)])
        self.ln_f = nn.LayerNorm(emb_dim)  # final layer norm
        self.lm_head = nn.Linear(emb_dim, vocab_size)

        self.block_size = block_size

    def forward(self, idx, targets=None):
        B, T = idx.shape
        assert T <= self.block_size, f"Cannot forward, sequence length {T} > block size {self.block_size}"
        
        token_emb = self.token_embedding(idx)  # (B, T, emb_dim)
        pos_emb = self.position_embedding(torch.arange(T, device=idx.device))  # (T, emb_dim)
        x = token_emb + pos_emb  # (B, T, emb_dim)

        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)  # (B, T, vocab_size)

        if targets is None:
            loss = None
        else:
            # Reshape logits and targets for cross-entropy
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.block_size:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :]  # focus only on last time step
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)
        return idx
