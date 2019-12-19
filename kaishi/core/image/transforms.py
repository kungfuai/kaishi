def transform_fix_rotation(self):
    """Fix rotations of each image given pre-determined labels."""
    if not self.labeled:
        self.predict_and_label()
        self.labeled = True

    for f in self.files:
        if 'RECTIFIED' in f.labels:
            continue
        elif 'ROTATED_RIGHT' in f.labels:
            f.rotate(90)
            f.remove_label('ROTATED_RIGHT')
        elif 'ROTATED_LEFT' in f.labels:
            f.rotate(270)
            f.remove_label('ROTATED_LEFT')
        elif 'UPSIDE_DOWN' in f.labels:
            f.rotate(180)
            f.remove_label('UPSIDE_DOWN')
        f.add_label('RECTIFIED')

    return
