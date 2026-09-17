export type TeaType =
  | 'green'
  | 'white'
  | 'yellow'
  | 'oolong'
  | 'red'
  | 'puer'
  | 'herbal';

export type Teaware =
  | 'gaiwan'
  | 'teapot'
  | 'brewer'
  | 'cup'
  | 'other';

export interface Tea {
  id: number;
  name: string;
  type: TeaType;
  rating: number;
  teaware: Teaware;
  description: string;
}