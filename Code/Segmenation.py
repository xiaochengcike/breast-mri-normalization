import numpy as np
def Generator_multichannels(image, sizeofchunk, sizeofchunk_expand,numofchannels): 
    sizeofimage = np.shape(image)[1:4]
            
    nb_chunks = (np.ceil(np.array(sizeofimage)/float(sizeofchunk))).astype(int)
    
    pad_image = np.zeros(([numofchannels,nb_chunks[0]*sizeofchunk,nb_chunks[1]*sizeofchunk,nb_chunks[2]*sizeofchunk]), dtype='float32')
    pad_image[:,:sizeofimage[0], :sizeofimage[1], :sizeofimage[2]] = image
            
    width = int(np.ceil((sizeofchunk_expand-sizeofchunk)/2.0))
            
    size_pad_im = np.shape(pad_image)[1:4]
    size_expand_im = np.array(size_pad_im) + 2 * width
    expand_image = np.zeros(([numofchannels,size_expand_im[0],size_expand_im[1],size_expand_im[2]]), dtype='float32')
    expand_image[:,width:-width, width:-width, width:-width] = pad_image
  
            
    batchsize = np.prod(nb_chunks)
    idx_chunk = 0
    chunk_batch = np.zeros((batchsize,numofchannels,sizeofchunk_expand,sizeofchunk_expand,sizeofchunk_expand),dtype='float32')
    idx_xyz = np.zeros((batchsize,3),dtype='uint16')
    for x_idx in range(nb_chunks[0]):
        for y_idx in range(nb_chunks[1]):
            for z_idx in range(nb_chunks[2]):
                
                idx_xyz[idx_chunk,:] = [x_idx,y_idx,z_idx]
                        
                         

                chunk_batch[idx_chunk,:,...] = expand_image[:,x_idx*sizeofchunk:x_idx*sizeofchunk+sizeofchunk_expand,\
                           y_idx*sizeofchunk:y_idx*sizeofchunk+sizeofchunk_expand,\
                           z_idx*sizeofchunk:z_idx*sizeofchunk+sizeofchunk_expand]             
                        
                idx_chunk += 1
    
    return chunk_batch, nb_chunks, idx_xyz, sizeofimage    

def Chunks_Image(segment_chunks, nb_chunks, sizeofchunk, sizeofchunk_expand, idx_xyz, sizeofimage):
    
    batchsize = np.size(segment_chunks,0)
    width = int(np.ceil((sizeofchunk_expand-sizeofchunk)/2.0))
    segment_image = np.zeros((nb_chunks[0]*sizeofchunk,nb_chunks[1]*sizeofchunk,nb_chunks[2]*sizeofchunk))
    
    for idx_chunk in range(batchsize):
        
        idx_low = idx_xyz[idx_chunk,:] * sizeofchunk
        idx_upp = (idx_xyz[idx_chunk,:]+1) * sizeofchunk
        
        segment_image[idx_low[0]:idx_upp[0],idx_low[1]:idx_upp[1],idx_low[2]:idx_upp[2]] = \
        segment_chunks[idx_chunk,0,...][width:-width,width:-width,width:-width]
        

    segment_image = segment_image[:sizeofimage[0], :sizeofimage[1], :sizeofimage[2]]
    return segment_image

