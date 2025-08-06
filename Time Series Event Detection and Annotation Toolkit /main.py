import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN

# --- Parameters ---
np.random.seed(42)
TIME_STEPS = 350
y = np.sin(0.036*np.arange(TIME_STEPS)) + np.random.randn(TIME_STEPS)*0.15
y[90] += 3     # Positive spike
y[160] -= 2.5  # Negative spike
y[190:195] += 2  # Mini regime change
y[308] -= 3.4

print("=== Time Series Event Detection Toolkit ===")
use_file = input("Load from CSV? (y/n): ").strip().lower().startswith("y")
if use_file:
    fname = input("CSV filename (column must be y): ").strip()
    y = pd.read_csv(fname)["y"].values

plt.plot(y, label='Signal')
plt.title("Time Series: Click close window to annotate")
plt.show()

annotations = []
while True:
    ind = input("Annotate event at index (blank to end): ").strip()
    if not ind:
        break
    ind = int(ind)
    label = input("  Label (e.g. spike, drop, regime): ").strip()
    desc = input("  (Optional) Note: ").strip()
    annotations.append({"index": ind, "label": label, "note": desc})

# Feature extraction for similarity: window around event
W = 18
vectors = []
for ann in annotations:
    ix = ann["index"]
    seg = y[max(0,ix-W):min(len(y),ix+W+1)]
    if len(seg) < 2*W+1:
        # Pad for boundary
        seg = np.pad(seg, (max(0,W-ix), max(0,W+ix+1-len(y))), constant_values=0)
    vectors.append(seg)

# Automatic pattern-matching
print("\nSearching for similar events in full series...")
all_segments = []
indices = []
for i in range(W, len(y)-W):
    seg = y[i-W:i+W+1]
    all_segments.append(seg)
    indices.append(i)
# Compute max similarity to each annotated event
all_segments_arr = np.stack(all_segments)
vectors_arr = np.stack(vectors)
sims = cosine_similarity(all_segments_arr, vectors_arr)  # shape: [n_points, n_annotations]
max_sim = np.max(sims, axis=1)
match_inds = [indices[i] for i in np.where(max_sim>0.96)[0]]
match_inds_set = set(match_inds)
# Discard near-duplicates from close proximity
auto_detected = []
for ix in sorted(match_inds):
    if annotations and any(abs(a["index"]-ix)<=W for a in annotations):
        continue
    if not auto_detected or abs(auto_detected[-1]-ix) > W:
        auto_detected.append(ix)

print(f"Automatically detected {len(auto_detected)} similar events.")
for ix in auto_detected:
    print(f"Auto-detected event at {ix}")

# Optional: Cluster all events (DBSCAN)
X_to_cluster = np.concatenate([vectors_arr] + [all_segments_arr[np.where(max_sim>0.96)]])
clustering = DBSCAN(eps=1.5, min_samples=2).fit(X_to_cluster)
print(f"\nClustered event segments, labels: {set(clustering.labels_)}")

# Create event timeline export
timeline = annotations + [{"index": int(ix), "label": "auto_match", "note": ""} for ix in auto_detected]
timeline = sorted(timeline, key=lambda x: x["index"])

out_csv = "event_timeline.csv"
out_json = "event_timeline.json"
pd.DataFrame(timeline).to_csv(out_csv, index=False)
with open(out_json, "w") as f:
    json.dump(timeline, f, indent=2)
print(f"\nExported event timeline to {out_csv} and {out_json}")

# Visualization
plt.figure(figsize=(12,5))
plt.plot(y, label='Signal')
if timeline:
    inds = [ev["index"] for ev in timeline]
    labs = [ev["label"] for ev in timeline]
    plt.scatter(inds, y[inds], c='red', label='Events')
    for i,ix in enumerate(inds):
        plt.annotate(labs[i], (ix, y[ix]), fontsize=8)
plt.title("Events (Annotated + Detected)")
plt.tight_layout()
plt.savefig("annotated_events.png")
plt.show()
print("Event chart saved as annotated_events.png")
