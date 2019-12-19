

def get_selected_vert_sequences(verts, ensure_seq_len=False, debug=False):
    """
    return sorted lists of vertices, where vertices are considered connected if their edges are selected, and faces are not selected
    """
    sequences = []

    # if edge loops are non-cyclic, it matters at what vert you start the sorting
    noncyclicstartverts = [v for v in verts if len([e for e in v.link_edges if e.select]) == 1]

    if noncyclicstartverts:
        v = noncyclicstartverts[0]

    # in cyclic edge loops, any vert works
    else:
        v = verts[0]

    seq = []

    while verts:
        seq.append(v)

        # safty precaution,for EPanel, where people may select intersecting edge loops
        if v not in verts:
            break

        else:
            verts.remove(v)

        if v in noncyclicstartverts:
            noncyclicstartverts.remove(v)

        nextv = [e.other_vert(v) for e in v.link_edges if e.select and e.other_vert(v) not in seq]

        # next vert in sequence
        if nextv:
            v = nextv[0]

        # finished a sequence
        else:
            # determine cyclicity
            cyclic = True if len([e for e in v.link_edges if e.select]) == 2 else False

            # store sequence and cyclicity
            sequences.append((seq, cyclic))

            # start a new sequence, if there are still verts left
            if verts:
                if noncyclicstartverts:
                    v = noncyclicstartverts[0]
                else:
                    v = verts[0]

                seq = []

    # again for EPanel, make sure sequences are longer than one vert
    if ensure_seq_len:
        seqs = []

        for seq, cyclic in sequences:
            if len(seq) > 1:
                seqs.append((seq, cyclic))

        sequences = seqs

    if debug:
        for seq, cyclic in sequences:
            print(cyclic, [v.index for v in seq])

    return sequences
